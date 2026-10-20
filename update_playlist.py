import urllib.request
import re

# সোর্স প্লেলিস্টের লিংক
SOURCE_URL = "https://raw.githubusercontent.com/sm-monirulislam/Toffee-Auto-Update/refs/heads/main/toffee_playlist.m3u"
OUTPUT_FILE = "saff_live_1.m3u"
NEW_GROUP = 'group-title="LIVE SPORTS"'

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
        
        # 'SAFF Live 1' চ্যানেল খুঁজে বের করা
        if line.startswith("#EXTINF") and "saff live 1" in line.lower():
            # যদি আগে থেকেই group-title থাকে, তবে তা পরিবর্তন করবে; না থাকলে নতুন যুক্ত করবে
            if 'group-title="' in line:
                line = re.sub(r'group-title="[^"]*"', NEW_GROUP, line)
            else:
                # #EXTINF:-1 এর পর group-title বসানো
                line = line.replace("#EXTINF:-1", f"#EXTINF:-1 {NEW_GROUP}")
            
            filtered_lines.append(line)
            
            # ট্যাগের পরবর্তী সব প্রয়োজনীয় লাইন (যেমন #EXTVLCOPT বা ডাইরেক্ট স্ট্রিম URL) সংগ্রহ করা
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if not next_line:
                    i += 1
                    continue
                
                filtered_lines.append(next_line)
                # যদি এটি স্ট্রিম ইউআরএল হয় (যা # দিয়ে শুরু হয় না), তবে এটি যুক্ত করে লুপ শেষ হবে
                if not next_line.startswith("#"):
                    break
                i += 1
                
            found = True
            break
        i += 1

    if found:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(filtered_lines) + "\n")
        print(f"Successfully extracted 'SAFF Live 1' with group-title 'LIVE SPORTS' to {OUTPUT_FILE}")
    else:
        print("Channel 'SAFF Live 1' not found in the source playlist.")

if __name__ == "__main__":
    extract_channel()
