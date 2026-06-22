import requests

SOURCE_URL = "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update-Playlist/refs/heads/main/OTT_Navigator.m3u"
OUTPUT_FILE = "toffee.m3u"

CUSTOM_CHANNELS = [
    {
        "extinf": '#EXTINF:-1 group-title="PROMO" tvg-logo="https://i.postimg.cc/13XVVyg3/1773936967533.png",STABLE-SPORTS TV',
        "url": "http://198.195.239.50:8095/StarSports2/tracks-v1a1/mono.m3u8"
    },
    {
        "extinf": '#EXTINF:-1 group-title="ENTERTAINMENT CHANNELS" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/Colors_Bengali_HD.png",Colors Bangla HD',
        "url": "http://main.epgmaker.com/live/y49sz6KMQs/6115263489/532.ts"
    },
    {
        "extinf": '#EXTINF:-1 group-title="ENTERTAINMENT CHANNELS" tvg-logo="https://jiotvimages.cdn.jio.com/dare_images/images/ZeeBangla.png",ZEE Bangla HD',
        "url": "http://main.epgmaker.com/live/y49sz6KMQs/6115263489/536.ts"
    }
]


def update_playlist():
    r = requests.get(SOURCE_URL)
    r.raise_for_status()

    lines = r.text.splitlines()

    channels = []
    current = None

    for line in lines:
        if line.startswith("#EXTINF"):
            if current:
                channels.append(current)
            current = [line]
        elif current is not None:
            current.append(line)

    if current:
        channels.append(current)

    # আসল প্রথম channel remove
    if len(channels) > 0:
        channels.pop(0)

    output = ["#EXTM3U"]

    for ch in channels:
        output.extend(ch)

    # নিজের channel শেষে add
    for c in CUSTOM_CHANNELS:
        output.append(c["extinf"])
        output.append(c["url"])

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output))


if __name__ == "__main__":
    update_playlist()
