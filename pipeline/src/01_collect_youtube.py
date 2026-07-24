"""Paso 1 — Recolección de comentarios de YouTube.

Estrategia:
  1. search.list por cada query del config (videos dentro de la ventana de estudio)
  2. Videos de canales monitoreados cuyo título mencione al sujeto
  3. commentThreads.list por video (con paginación) -> data/raw/comments.parquet

Cuota: search.list = 100 unidades, commentThreads.list = 1 unidad.
Con la cuota gratuita diaria (10,000) alcanzan ~60 búsquedas + ~4,000 páginas
de comentarios (~400,000 comentarios). Si te quedas sin cuota, el script
guarda el progreso y puedes relanzarlo al día siguiente: no re-descarga
videos ya procesados.

Uso:
    export YT_API_KEY='...'
    python src/01_collect_youtube.py
"""
import json
import time
from datetime import datetime, timezone

import pandas as pd
from googleapiclient.errors import HttpError

from utils import DATA_RAW, get_youtube_client, load_config, normalize_text

CFG = load_config()
YT_CFG = CFG["youtube"]
CHECKPOINT = DATA_RAW / "collected_video_ids.json"
OUT_COMMENTS = DATA_RAW / "comments.parquet"
OUT_VIDEOS = DATA_RAW / "videos.parquet"


def _iso(d: str) -> str:
    return f"{d}T00:00:00Z"


def search_videos(yt) -> list[dict]:
    """Busca videos relevantes por query dentro de la ventana de estudio."""
    videos, seen = [], set()
    for query in YT_CFG["search_queries"]:
        page_token, fetched = None, 0
        while fetched < YT_CFG["max_videos_per_query"]:
            try:
                resp = yt.search().list(
                    q=query,
                    type="video",
                    part="snippet",
                    maxResults=50,
                    order="relevance",
                    relevanceLanguage="es",
                    regionCode="DO",
                    publishedAfter=_iso(CFG["study"]["date_start"]),
                    publishedBefore=_iso(CFG["study"]["date_end"]),
                    pageToken=page_token,
                ).execute()
            except HttpError as e:
                print(f"  [!] Error en búsqueda '{query}': {e}")
                break
            for item in resp.get("items", []):
                vid = item["id"]["videoId"]
                if vid in seen:
                    continue
                seen.add(vid)
                videos.append(
                    {
                        "video_id": vid,
                        "title": item["snippet"]["title"],
                        "channel": item["snippet"]["channelTitle"],
                        "channel_id": item["snippet"]["channelId"],
                        "published_at": item["snippet"]["publishedAt"],
                        "found_via": f"search:{query}",
                    }
                )
            fetched += len(resp.get("items", []))
            page_token = resp.get("nextPageToken")
            if not page_token:
                break
        print(f"[search] '{query}': {fetched} videos")
    return videos


def channel_videos(yt) -> list[dict]:
    """Videos recientes de canales monitoreados que mencionen al sujeto."""
    subject_kw = [normalize_text(k) for k in CFG["relevance"]["subject_keywords"]]
    videos = []
    for ch in YT_CFG["channels"]:
        if not ch.get("id"):
            continue
        try:
            # uploads playlist = channel_id con 'UU' en vez de 'UC'
            playlist_id = "UU" + ch["id"][2:]
            page_token, keep = None, 0
            for _ in range(6):  # hasta 300 videos recientes por canal
                resp = yt.playlistItems().list(
                    playlistId=playlist_id,
                    part="snippet",
                    maxResults=50,
                    pageToken=page_token,
                ).execute()
                for item in resp.get("items", []):
                    sn = item["snippet"]
                    title_norm = normalize_text(sn["title"])
                    if any(k in title_norm for k in subject_kw):
                        videos.append(
                            {
                                "video_id": sn["resourceId"]["videoId"],
                                "title": sn["title"],
                                "channel": ch["name"],
                                "channel_id": ch["id"],
                                "published_at": sn["publishedAt"],
                                "found_via": f"channel:{ch['name']}",
                            }
                        )
                        keep += 1
                page_token = resp.get("nextPageToken")
                if not page_token:
                    break
            print(f"[channel] {ch['name']}: {keep} videos relevantes")
        except HttpError as e:
            print(f"  [!] Error en canal {ch['name']}: {e}")
    return videos


def fetch_comments(yt, video: dict) -> list[dict]:
    comments, page_token = [], None
    while len(comments) < YT_CFG["max_comments_per_video"]:
        try:
            resp = yt.commentThreads().list(
                videoId=video["video_id"],
                part="snippet,replies",
                maxResults=100,
                textFormat="plainText",
                pageToken=page_token,
            ).execute()
        except HttpError as e:
            if "commentsDisabled" in str(e):
                return comments
            if "quotaExceeded" in str(e):
                raise
            print(f"  [!] {video['video_id']}: {e}")
            return comments

        for th in resp.get("items", []):
            top = th["snippet"]["topLevelComment"]["snippet"]
            comments.append(_row(top, video, is_reply=False))
            for rep in th.get("replies", {}).get("comments", []):
                comments.append(_row(rep["snippet"], video, is_reply=True))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return comments


def _row(sn: dict, video: dict, is_reply: bool) -> dict:
    return {
        "comment_id": sn.get("parentId", "") + ("_r" if is_reply else ""),
        "video_id": video["video_id"],
        "video_title": video["title"],
        "channel": video["channel"],
        "author": sn.get("authorDisplayName", ""),
        "text": sn.get("textDisplay", ""),
        "like_count": sn.get("likeCount", 0),
        "published_at": sn.get("publishedAt", ""),
        "is_reply": is_reply,
        "found_via": video["found_via"],
    }


def main():
    yt = get_youtube_client()
    done = set(json.loads(CHECKPOINT.read_text())) if CHECKPOINT.exists() else set()

    videos = search_videos(yt) + channel_videos(yt)
    # dedup por video_id conservando primera aparición
    videos = list({v["video_id"]: v for v in videos}.values())
    pd.DataFrame(videos).to_parquet(OUT_VIDEOS, index=False)
    print(f"\nTotal videos únicos: {len(videos)} ({len(done)} ya procesados)\n")

    all_comments = []
    if OUT_COMMENTS.exists():
        all_comments = [pd.read_parquet(OUT_COMMENTS)]

    try:
        for i, video in enumerate(v for v in videos if v["video_id"] not in done):
            rows = fetch_comments(yt, video)
            if rows:
                all_comments.append(pd.DataFrame(rows))
            done.add(video["video_id"])
            print(f"[{i+1}] {video['title'][:60]:60s} -> {len(rows)} comentarios")
            time.sleep(0.1)
    except HttpError:
        print("\n[!] Cuota agotada. Progreso guardado — relanza mañana.")
    finally:
        if all_comments:
            df = pd.concat(all_comments, ignore_index=True)
            df = df.drop_duplicates(subset=["video_id", "author", "text", "published_at"])
            df.to_parquet(OUT_COMMENTS, index=False)
            print(f"\nGuardado: {OUT_COMMENTS} ({len(df):,} comentarios)")
        CHECKPOINT.write_text(json.dumps(sorted(done)))
        print(f"Checkpoint: {len(done)} videos procesados | {datetime.now(timezone.utc)}")


if __name__ == "__main__":
    main()
