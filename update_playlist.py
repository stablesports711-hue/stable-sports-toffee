import urllib.request

# সোর্স প্লেলিস্টের লিংক
SOURCE_URL = "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update/refs/heads/main/toffee_playlist.m3u"
OUTPUT_FILE = "saff_live_1.m3u"

def extract_channel():
    print("Downloading source playlist...")
    req = urllib.request.Request(
        SOURCE_URL,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
    except Exception as e:
        print(f"Error downloading playlist: {e}")
        return

    lines = content.splitlines()
    filtered_lines = ["#EXTM3U"]
    
    found = False
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # এখানে 'SAFF Live 1' খঁুজে বের করা হচ্ছে (বড়-ছোট হাতের অক্ষর এড়িয়ে চলার জন্য .lower() ব্যবহার করা যেতে পারে)
        if line.startswith("#EXTINF") and "saff live 1" in line.lower():
            filtered_lines.append(line)
            # পরবর্তী লাইনটি স্ট্রিম লিংক হলে তা যুক্ত করা
            if i + 1 < len(lines) and not lines[i + 1].startswith("#"):
                filtered_lines.append(lines[i + 1].strip())
            found = True
            break
        i += 1

    if found:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(filtered_lines) + "\n")
        print(f"Successfully extracted 'SAFF Live 1' to {OUTPUT_FILE}")
    else:
        print("Channel 'SAFF Live 1' not found in the source playlist.")

if __name__ == "__main__":
    extract_channel()
