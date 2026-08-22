import requests
import re

SOURCE_URL = "https://raw.githubusercontent.com/srhady/Hady/refs/heads/main/akash_live.m3u"
OUTPUT_FILE = "PL Live.m3u"

# =========================================================
# CUSTOM CHANNEL
# এখানে তোমার ১টি নিজের চ্যানেলের তথ্য বসাবে
# =========================================================

CUSTOM_CHANNEL = {
    "name": "MY CUSTOM CHANNEL",
    "logo": "https://example.com/logo.png",
    "url": "https://example.com/stream.m3u8"
}


def get_pl_live_channels():

    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()

    lines = response.text.splitlines()

    channels = []
    current_channel = []

    for line in lines:

        if line.startswith("#EXTINF:"):

            # আগের channel পরীক্ষা
            if current_channel:

                extinf = current_channel[0]

                # শুধু PL Live নামের channel
                if "PL Live" in extinf:
                    channels.append(current_channel)

            current_channel = [line]

        elif current_channel:
            current_channel.append(line)

    # শেষ channel
    if current_channel:

        extinf = current_channel[0]

        if "PL Live" in extinf:
            channels.append(current_channel)

    return channels


def change_group_title(extinf):

    # পুরোনো group-title থাকলে LIVE SPORTS করা
    if 'group-title=' in extinf:

        extinf = re.sub(
            r'group-title="[^"]*"',
            'group-title="LIVE SPORTS"',
            extinf
        )

    else:

        extinf = extinf.replace(
            '#EXTINF:-1',
            '#EXTINF:-1 group-title="LIVE SPORTS"',
            1
        )

    return extinf


def update_playlist():

    output = [
        "#EXTM3U",
        "#PLAYLIST:PL Live"
    ]

    # =====================================================
    # SOURCE CHANNELS
    # =====================================================

    channels = get_pl_live_channels()

    for channel in channels:

        if not channel:
            continue

        # EXTINF পরিবর্তন
        channel[0] = change_group_title(channel[0])

        output.extend(channel)

    # =====================================================
    # CUSTOM CHANNEL
    # =====================================================

    custom_extinf = (
        '#EXTINF:-1 '
        'group-title="LIVE SPORTS" '
        f'tvg-logo="{CUSTOM_CHANNEL["logo"]}",'
        f'{CUSTOM_CHANNEL["name"]}'
    )

    output.append(custom_extinf)
    output.append(CUSTOM_CHANNEL["url"])

    # =====================================================
    # SAVE
    # =====================================================

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write("\n".join(output) + "\n")

    source_count = len(channels)

    print(f"Source PL Live channels : {source_count}")
    print("Custom channel          : 1")
    print(f"Total channels          : {source_count + 1}")
    print(f"Output file             : {OUTPUT_FILE}")


if __name__ == "__main__":
    update_playlist()
