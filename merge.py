 import requests
from urllib.parse import urljoin
from pathlib import Path

SOURCES = [
    ("1st Part", "https://img.refooty.com/m3u8/14686-Vtynu.m3u8"),
    ("2nd Part", "https://img.refooty.com/m3u8/14688-mRRNn.m3u8"),
    ("Extra Time", "https://img.refooty.com/m3u8/14689-2eydem3u8-sN8bm.m3u8"),
    ("Ceremony", "https://img.refooty.com/m3u8/14690-dmzmzm3u8-VsMoJ.m3u8"),
]

OUTPUT = "final.m3u8"

headers = {
    "User-Agent": "Mozilla/5.0"
}

all_segments = []
target_duration = 0

for name, url in SOURCES:
    print("Processing:", name)

    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()

    lines = [x.strip() for x in r.text.splitlines() if x.strip()]

    current_duration = None

    for line in lines:

        if line.startswith("#EXT-X-TARGETDURATION:"):
            try:
                td = int(line.split(":", 1)[1])
                target_duration = max(target_duration, td)
            except:
                pass

        elif line.startswith("#EXTINF:"):
            try:
                current_duration = float(
                    line.split(":", 1)[1].split(",", 1)[0]
                )
            except:
                current_duration = None

        elif not line.startswith("#"):
            if current_duration is not None:
                segment_url = urljoin(url, line)

                all_segments.append({
                    "duration": current_duration,
                    "url": segment_url
                })

                current_duration = None

    # Part শেষ হওয়ার পরে discontinuity
    if name != SOURCES[-1][0]:
        all_segments.append({
            "discontinuity": True
        })

if not all_segments:
    raise RuntimeError("No video segments found.")

if target_duration == 0:
    target_duration = 10

output = [
    "#EXTM3U",
    "#EXT-X-VERSION:3",
    f"#EXT-X-TARGETDURATION:{target_duration}",
    "#EXT-X-MEDIA-SEQUENCE:0",
    "#EXT-X-PLAYLIST-TYPE:VOD"
]

for item in all_segments:

    if item.get("discontinuity"):
        output.append("#EXT-X-DISCONTINUITY")
    else:
        output.append(f"#EXTINF:{item['duration']:.3f},")
        output.append(item["url"])

output.append("#EXT-X-ENDLIST")

Path(OUTPUT).write_text(
    "\n".join(output) + "\n",
    encoding="utf-8"
)

print("Created:", OUTPUT)
print("Total segments:", len(all_segments))
