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

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

all_segments = []
target_duration = 0

for name, playlist_url in SOURCES:
    print(f"Processing: {name}")

    response = requests.get(
        playlist_url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    lines = response.text.splitlines()
    current_duration = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("#EXT-X-TARGETDURATION:"):
            try:
                value = int(line.split(":", 1)[1])
                target_duration = max(target_duration, value)
            except ValueError:
                pass

        elif line.startswith("#EXTINF:"):
            try:
                current_duration = float(
                    line.split(":", 1)[1].split(",", 1)[0]
                )
            except ValueError:
                current_duration = None

        elif not line.startswith("#"):
            if current_duration is not None:
                segment_url = urljoin(playlist_url, line)

                all_segments.append(
                    ("segment", current_duration, segment_url)
                )

                current_duration = None

    if name != SOURCES[-1][0]:
        all_segments.append(("discontinuity", 0, ""))

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

for item_type, duration, url in all_segments:
    if item_type == "discontinuity":
        output.append("#EXT-X-DISCONTINUITY")
    else:
        output.append(f"#EXTINF:{duration:.3f},")
        output.append(url)

output.append("#EXT-X-ENDLIST")

Path(OUTPUT).write_text(
    "\n".join(output) + "\n",
    encoding="utf-8"
)

print("Successfully created:", OUTPUT)
print("Total segments:", sum(
    1 for item in all_segments if item[0] == "segment"
))
