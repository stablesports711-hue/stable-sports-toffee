import requests
import os

SOURCE_URL = "https://raw.githubusercontent.com/srhady/toffee-bd/refs/heads/main/toffee_playlist.m3u"

OUTPUT_FILE = "toffee.m3u"
CUSTOM_FILE = "custom_channels.m3u"


def get_channels_from_text(text):
    lines = text.splitlines()

    channels = []
    current = None

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith("#EXTINF"):
            if current:
                channels.append(current)

            current = [line]

        elif current is not None:
            current.append(line)

    if current:
        channels.append(current)

    return channels


def update_playlist():

    # সোর্স Playlist ডাউনলোড
    r = requests.get(SOURCE_URL, timeout=30)
    r.raise_for_status()

    source_channels = get_channels_from_text(r.text)

    output = ["#EXTM3U"]

    # সোর্সের প্রথম চ্যানেল বাদ
    for channel in source_channels[1:]:
        output.extend(channel)

    # custom_channels.m3u থেকে নিজের চ্যানেল যোগ
    if os.path.exists(CUSTOM_FILE):

        with open(CUSTOM_FILE, "r", encoding="utf-8") as f:
            custom_text = f.read()

        custom_channels = get_channels_from_text(custom_text)

        for channel in custom_channels:
            output.extend(channel)

    # Final Playlist তৈরি
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print("Playlist updated successfully!")


if __name__ == "__main__":
    update_playlist()
