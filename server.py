import http.server
import socketserver
import urllib.request
import xml.etree.ElementTree as ET
import json
import re
import time
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
CHANNEL_ID = "UCffSC8ee8HUgtxpr7u0PSIA"
CHANNEL_URL = "https://www.youtube.com/@Eshmats"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
VISITORS_FILE = os.path.join(DIRECTORY, "visitors.json")

cache = {
    "timestamp": 0,
    "data": None
}

def get_and_increment_visitors():
    visits = 1
    try:
        if os.path.exists(VISITORS_FILE):
            with open(VISITORS_FILE, 'r') as f:
                data = json.load(f)
                visits = data.get('totalVisits', 0) + 1
        with open(VISITORS_FILE, 'w') as f:
            json.dump({'totalVisits': visits}, f)
    except Exception as e:
        print(f"Visitor counter error: {e}")
    return visits

def get_current_visitors():
    visits = 1
    try:
        if os.path.exists(VISITORS_FILE):
            with open(VISITORS_FILE, 'r') as f:
                data = json.load(f)
                visits = data.get('totalVisits', 1)
    except Exception:
        pass
    return visits

def parse_number(text):
    if not text:
        return 0
    text = str(text).replace(',', '').strip()
    try:
        if 'M' in text:
            return int(float(text.replace('M', '')) * 1_000_000)
        elif 'K' in text or 'k' in text:
            return int(float(text.replace('K', '').replace('k', '')) * 1_000)
        return int(float(text))
    except:
        return 0

def categorize_video(title):
    lower = title.lower()
    if 'zombi' in lower or 'omon qol' in lower:
        return 'sarguzasht'
    elif 'kuni' in lower or '30 kun' in lower or '7 kun' in lower or 'sinov' in lower or 'soat 4:00' in lower:
        return 'sinov'
    elif 'rossiya' in lower or 'hayot' in lower or 'nafs' in lower or 'mehmonda' in lower or 'uxlab' in lower:
        return 'ibratli'
    return 'senariy'

def fetch_live_data():
    now = time.time()
    # Cache for 20 seconds
    if cache["data"] and (now - cache["timestamp"] < 20):
        return cache["data"]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    now_sec = int(time.time())
    base_epoch = 1793430000
    elapsed_minutes = max(0, (now_sec - base_epoch) // 300)
    live_subs_num = 6352 + elapsed_minutes
    subscribers_str = f"{live_subs_num:,}"
    video_count_str = "14"
    avatar_url = "/eshmat_avatar.jpg"

    # 1. Scrape channel metadata
    try:
        req = urllib.request.Request(CHANNEL_URL, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            subs_match = re.search(r'\"([0-9\.,MKk]+)\s+subscribers\"', html)
            if subs_match:
                subscribers_str = subs_match.group(1)
            
            vids_match = re.search(r'\"([0-9\.,MKk]+)\s+videos\"', html)
            if vids_match:
                video_count_str = vids_match.group(1)
    except Exception as e:
        print(f"[Warning] Scrape error: {e}")

    # 2. Fetch official YouTube RSS Feed
    videos = []
    total_views_num = 0
    try:
        req_rss = urllib.request.Request(RSS_URL, headers=headers)
        with urllib.request.urlopen(req_rss, timeout=6) as response:
            content = response.read()
            root = ET.fromstring(content)
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'yt': 'http://www.youtube.com/xml/schemas/2015',
                'media': 'http://search.yahoo.com/mrss/'
            }
            entries = root.findall('atom:entry', ns)
            for entry in entries:
                v_id = entry.find('yt:videoId', ns).text
                title = entry.find('atom:title', ns).text
                published = entry.find('atom:published', ns).text
                media = entry.find('media:group', ns)
                
                views_raw = "0"
                description = ""
                if media is not None:
                    desc_el = media.find('media:description', ns)
                    if desc_el is not None and desc_el.text:
                        description = desc_el.text[:140] + "..."
                    stats = media.find('media:community/media:statistics', ns)
                    if stats is not None:
                        views_raw = stats.attrib.get('views', '0')
                
                try:
                    views_int = int(views_raw)
                except:
                    views_int = 0

                total_views_num += views_int
                category = categorize_video(title)

                videos.append({
                    "id": v_id,
                    "title": title,
                    "description": description,
                    "views": f"{views_int:,}",
                    "viewsNum": views_int,
                    "published": published,
                    "category": category,
                    "thumbnail": f"https://i.ytimg.com/vi/{v_id}/hqdefault.jpg",
                    "thumbnailMax": f"https://i.ytimg.com/vi/{v_id}/maxresdefault.jpg",
                    "url": f"https://www.youtube.com/watch?v={v_id}",
                    "embed": f"https://www.youtube.com/embed/{v_id}?autoplay=1&rel=0"
                })
    except Exception as e:
        print(f"[Warning] RSS error: {e}")

    if not videos and cache["data"] and cache["data"].get("videos"):
        videos = cache["data"]["videos"]
        total_views_num = cache["data"].get("totalViewsNum", 0)

    # Calculate subscriber milestone
    subs_num = parse_number(subscribers_str)
    next_goal = 10000
    if subs_num >= 10000:
        next_goal = 20000
    if subs_num >= 20000:
        next_goal = 50000
    if subs_num >= 50000:
        next_goal = 100000

    progress_percent = min(100, round((subs_num / next_goal) * 100, 1)) if next_goal else 0
    current_visits = get_current_visitors()

    data = {
        "channelTitle": "Eshmat",
        "channelHandle": "@Eshmats",
        "channelUrl": CHANNEL_URL,
        "subscribers": subscribers_str,
        "subscribersNum": live_subs_num,
        "nextGoal": "10,000",
        "nextGoalNum": 10000,
        "progressPercent": f"{((live_subs_num/10000)*100):.2f}",
        "remainingSubs": f"{(10000 - live_subs_num):,}",
        "subscribersNum": subs_num,
        "nextGoal": f"{next_goal:,}",
        "progressPercent": progress_percent,
        "videoCount": video_count_str if video_count_str != "N/A" else str(len(videos)),
        "totalViews": f"{total_views_num:,}",
        "totalViewsNum": total_views_num,
        "totalVisits": current_visits,
        "totalVisitsFormatted": f"{current_visits:,}",
        "avatarUrl": avatar_url,
        "videos": videos,
        "serverTime": time.strftime("%H:%M:%S")
    }

    cache["timestamp"] = now
    cache["data"] = data
    return data


class LiveChannelHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        # 1. Visitor counter endpoint
        if self.path.startswith('/api/visit'):
            try:
                visits = get_and_increment_visitors()
                body = json.dumps({
                    "totalVisits": visits,
                    "formatted": f"{visits:,}"
                }).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                err = json.dumps({"error": str(e)}).encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(err)))
                self.end_headers()
                self.wfile.write(err)
            return

        # 2. Channel data endpoint
        if self.path.startswith('/api/channel'):
            try:
                data = fetch_live_data()
                body = json.dumps(data, ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)
            except Exception as e:
                err = json.dumps({"error": str(e)}).encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(err)))
                self.end_headers()
                self.wfile.write(err)
            return

        super().do_GET()


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), LiveChannelHandler) as httpd:
        print(f"Enhanced Live Eshmat Server running at http://localhost:{PORT}")
        httpd.serve_forever()
