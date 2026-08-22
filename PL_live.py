import requests
import re

SOURCE_URL = "https://raw.githubusercontent.com/srhady/Hady/refs/heads/main/akash_live.m3u"
OUTPUT_FILE = "PL Live.m3u"

# =========================================================
# CUSTOM CHANNEL
# এখানে তোমার নিজের ১টি চ্যানেলের তথ্য বসাবে
# =========================================================

CUSTOM_CHANNEL = {
    "name": "STABLE-SPORTS TV",
    "logo": "https://i.postimg.cc/13XVVyg3/1773936967533.png",
    "url": "https://res.cloudinary.com/qleik3si/video/upload/v1785235285/VN20260728_161756_ev6pow.mp4"
}


def update_playlist():

    print("Downloading source playlist...")

    response = requests.get(
        SOURCE_URL,
        timeout=60,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    lines = response.text.splitlines()

    output = [
        "#EXTM3U",
        "#PLAYLIST:PL Live"
    ]

    source_count = 0

    current = []

    for line in lines:

        if line.startswith("#EXTINF:"):

            # আগের channel save
            if current:

                extinf = current[0]

                if "PL Live" in extinf:

                    # group-title পরিবর্তন
                    extinf = re.sub(
                        r'group-title="[^"]*"',
                        'group-title="LIVE SPORTS"',
                        extinf
                    )

                    # group-title না থাকলে যোগ করবে
                    if 'group-title="LIVE SPORTS"' not in extinf:

                        extinf = extinf.replace(
                            "#EXTINF:-1",
                            '#EXTINF:-1 group-title="LIVE SPORTS"',
                            1
                        )

                    current[0] = extinf

                    output.extend(current)

                    source_count += 1

            current = [line]

        else:

            if current:
                current.append(line)

    # শেষ channel
    if current:

        extinf = current[0]

        if "PL Live" in extinf:

            extinf = re.sub(
                r'group-title="[^"]*"',
                'group-title="LIVE SPORTS"',
                extinf
            )

            if 'group-title="LIVE SPORTS"' not in extinf:

                extinf = extinf.replace(
                    "#EXTINF:-1",
                    '#EXTINF:-1 group-title="LIVE SPORTS"',
                    1
                )

            current[0] = extinf

            output.extend(current)

            source_count += 1

    # =====================================================
    # CUSTOM CHANNEL
    # =====================================================

    output.append(
        '#EXTINF:-1 group-title="LIVE SPORTS" '
        f'tvg-logo="{CUSTOM_CHANNEL["logo"]}",'
        f'{CUSTOM_CHANNEL["name"]}'
    )

    output.append(CUSTOM_CHANNEL["url"])

    # =====================================================
    # SAVE
    # =====================================================

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(output) + "\n")

    print("--------------------------------")
    print(f"PL Live channels : {source_count}")
    print("Custom channel  : 1")
    print(f"Total channels  : {source_count + 1}")
    print(f"Output file     : {OUTPUT_FILE}")
    print("--------------------------------")


if __name__ == "__main__":
    update_playlist()
