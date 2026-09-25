import requests
import base64
import json
import os
import urllib.parse
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# ==========================================
# 🌟 FIREBASE AUTO-URL ENGINE
# ==========================================

def get_firebase_base_url():
    print("🔵 [Auto] Fetching Dynamic URL from Firebase...")

    url = "https://firebaseremoteconfig.googleapis.com/v1/projects/963020218535/namespaces/firebase:fetch"

    headers = {
        "accept": "application/json",
        "x-android-package": "com.cricfy.tv",
        "x-goog-api-key": "AIzaSyAh9jkEU0E_UYxH0m_BKAt-uUSTiTPqhb8",
        "content-type": "application/json; charset=utf-8",
        "user-agent": "okhttp/5.0.0-alpha.12"
    }

    payload = {
        "appInstanceId": "e368b85dbdd148bdb73f1c5fecfdd3e2",
        "appInstanceIdToken": "",
        "appId": "1:963020218535:android:47ec53252c64fb3c9c7b82",
        "countryCode": "US",
        "languageCode": "en-US",
        "platformVersion": "30",
        "timeZone": "UTC",
        "appVersion": "5.0",
        "appBuild": "50",
        "packageName": "com.cricfy.tv",
        "sdkVersion": "22.1.0",
        "analyticsUserProperties": {}
    }

    try:
        res = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=10
        )

        if res.status_code == 200:
            data = res.json()
            entries = data.get("entries", {})

            url1 = entries.get("cric_api1")
            url2 = entries.get("cric_api2")

            for api_url in [url1, url2]:

                if api_url:
                    clean_url = api_url.rstrip("/")

                    print(f"   🔄 Checking URL: {clean_url} ...")

                    try:
                        requests.get(
                            clean_url,
                            headers=headers,
                            timeout=3
                        )

                        print(
                            f"   🎉 SUCCESS! Active Auto-URL Detected: {clean_url}"
                        )

                        return clean_url

                    except requests.exceptions.RequestException:
                        print(
                            f"   ⚠️ URL {clean_url} is dead/blocked."
                        )
                        continue

    except Exception as e:
        print(f"   ❌ Firebase Error: {e}")

    print("   ⚠️ Fetch failed or all URLs dead.")
    print("   🔄 Using fallback URL.")

    return "https://cfykskgdjk100.top"


# ==========================================
# CONFIGURATION
# ==========================================

BASE_URL = get_firebase_base_url()

KEYS_LIST = []

k1 = os.getenv("CRIC_KEY_1")
i1 = os.getenv("CRIC_IV_1")

if k1 and i1:
    KEYS_LIST.append({
        "key": k1,
        "iv": i1
    })


k2 = os.getenv("CRIC_KEY_2")
i2 = os.getenv("CRIC_IV_2")

if k2 and i2:
    KEYS_LIST.append({
        "key": k2,
        "iv": i2
    })


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; K) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0.0.0 "
        "Mobile Safari/537.36"
    ),
    "Referer": f"{BASE_URL}/",
    "Origin": BASE_URL,
    "Connection": "keep-alive"
}


# ==========================================
# 🔐 DECRYPT DATA
# ==========================================

def decrypt_data(encrypted_text):

    if not encrypted_text:
        return None

    try:

        clean_b64 = (
            encrypted_text
            .strip()
            .replace("\n", "")
            .replace("\r", "")
            .replace(" ", "")
            .replace("\t", "")
        )

        for creds in KEYS_LIST:

            try:

                k = bytes.fromhex(creds["key"])
                i = bytes.fromhex(creds["iv"])

                ciphertext = base64.b64decode(clean_b64)

                cipher = AES.new(
                    k,
                    AES.MODE_CBC,
                    i
                )

                decrypted = cipher.decrypt(ciphertext)

                return unpad(
                    decrypted,
                    AES.block_size
                ).decode("utf-8")

            except Exception:
                continue

    except Exception:
        pass

    return None


# ==========================================
# 🕐 UTC → IST TIME
# ==========================================

def convert_utc_to_ist(utc_time_str):

    try:

        if not utc_time_str:
            return ""

        clean_time = utc_time_str.split(" +")[0]

        utc_dt = datetime.strptime(
            clean_time,
            "%Y/%m/%d %H:%M:%S"
        )

        ist_dt = utc_dt + timedelta(
            hours=5,
            minutes=30
        )

        return ist_dt.strftime("%I:%M %p")

    except Exception:
        return ""


# ==========================================
# 📁 SMART FILENAME GENERATOR
# ==========================================

def get_smart_filename(event):

    guesses = []

    # --------------------------------------
    # 1. Event ID
    # --------------------------------------

    eid = str(
        event.get("id", "")
    )

    if eid:

        guesses.append(eid)
        guesses.append(
            f"match-{eid}"
        )


    # --------------------------------------
    # 2. Slug
    # --------------------------------------

    slug = (
        event.get("slug", "")
        .strip()
        .lower()
    )

    if slug:

        guesses.append(slug)

        guesses.append(
            urllib.parse.quote(slug)
        )

        guesses.append(
            slug.replace(" ", "-")
        )

        # Numbered variations

        for i in range(1, 7):

            guesses.append(
                urllib.parse.quote(
                    f"{slug} {i}"
                )
            )

            guesses.append(
                f"{slug.replace(' ', '-')}-{i}"
            )


    # --------------------------------------
    # 3. Team Names
    # --------------------------------------

    team_a = (
        event
        .get("eventInfo", {})
        .get("teamA", "")
        .strip()
        .lower()
    )

    team_b = (
        event
        .get("eventInfo", {})
        .get("teamB", "")
        .strip()
        .lower()
    )

    if team_a and team_b:

        t_a = team_a.replace(" ", "")
        t_b = team_b.replace(" ", "")

        base_vs = f"{t_a}-vs-{t_b}"

        guesses.append(base_vs)

        for i in range(1, 4):

            guesses.append(
                f"{base_vs}-{i}"
            )

    return guesses


# ==========================================
# 📺 FETCH MATCH STREAMS
# ==========================================

def fetch_match_streams(event):

    entries = []

    title = event.get(
        "title",
        "Live Event"
    )

    logo = (
        event
        .get("eventInfo", {})
        .get("eventLogo", "")
    )

    ist_time = convert_utc_to_ist(
        event.get("startTime", "")
    )

    if ist_time:

        group_title = (
            f"{title} [{ist_time}]"
        )

    else:

        group_title = title


    print(
        f"   📺 Processing: {group_title}"
    )


    valid_data = None

    filenames = get_smart_filename(
        event
    )


    # --------------------------------------
    # Search stream files
    # --------------------------------------

    for fname in filenames:

        try:

            for ext in [".txt", ""]:

                url = (
                    f"{BASE_URL}/channels/"
                    f"{fname}{ext}"
                )

                res = requests.get(
                    url,
                    headers=HEADERS,
                    timeout=3
                )


                if (
                    res.status_code == 200
                    and "google.com" not in res.text
                    and len(res.text) > 50
                ):

                    valid_data = decrypt_data(
                        res.text
                    )

                    if valid_data:

                        print(
                            f"      ✅ FOUND: "
                            f"{fname}{ext}"
                        )

                        break


            if valid_data:
                break


        except Exception:
            continue


    # --------------------------------------
    # No stream found
    # --------------------------------------

    if not valid_data:

        print(
            "      ❌ No stream file found."
        )

        return []


    # --------------------------------------
    # Parse stream data
    # --------------------------------------

    try:

        data = json.loads(
            valid_data
        )

        streams = data.get(
            "streamUrls",
            []
        )


        for s in streams:

            stream_name = s.get(
                "title",
                "Link"
            )

            raw_link = s.get(
                "link",
                ""
            )

            final_url = raw_link


            # --------------------------------
            # M3U Entry
            # --------------------------------

            entry = (
                f'#EXTINF:-1 '
                f'tvg-logo="{logo}" '
                f'group-title="{group_title}", '
                f'{title} ({stream_name})\n'
            )


            # --------------------------------
            # DRM
            # --------------------------------

            drm_key = s.get(
                "api"
            )

            if drm_key:

                entry += (
                    "#KODIPROP:"
                    "inputstream.adaptive."
                    "license_type=clearkey\n"
                )

                entry += (
                    f"#KODIPROP:"
                    "inputstream.adaptive."
                    f"license_key={drm_key}\n"
                )


            # --------------------------------
            # Stream URL
            # --------------------------------

            entry += (
                f"{final_url}\n"
            )


            entries.append(
                entry
            )


    except Exception as e:

        print(
            f"      ⚠️ JSON Error: {e}"
        )


    return entries


# ==========================================
# 🚀 MAIN
# ==========================================

def main():

    print(
        "🚀 Starting Generator "
        "(NO FILTER MODE)..."
    )

    all_entries = []


    try:

        # ----------------------------------
        # Check configuration
        # ----------------------------------

        if not BASE_URL:

            print(
                "❌ BASE_URL missing."
            )

            return


        if not KEYS_LIST:

            print(
                "❌ CRIC Secrets missing! "
                "Check GitHub Settings."
            )

            return


        # ----------------------------------
        # Fetch all live events
        # ----------------------------------

        print(
            f"🔵 Fetching live events from:"
            f"\n{BASE_URL}/categories/live-events.txt"
        )


        res = requests.get(
            f"{BASE_URL}/categories/live-events.txt",
            headers=HEADERS,
            timeout=15
        )


        if res.status_code != 200:

            print(
                f"❌ Failed to fetch categories: "
                f"{res.status_code}"
            )

            return


        # ----------------------------------
        # Decrypt category data
        # ----------------------------------

        raw_data = decrypt_data(
            res.text
        )


        if not raw_data:

            print(
                "❌ Category Decryption Failed"
            )

            return


        # ----------------------------------
        # Load events
        # ----------------------------------

        events = json.loads(
            raw_data
        )


        print(
            f"📋 Total events found: "
            f"{len(events)}"
        )


        # ==================================
        # 🔥 NO FILTER
        # ==================================

        for event in events:

            title = event.get(
                "title",
                "Live Event"
            )

            print(
                f"\n➡️ Checking event: {title}"
            )


            # এখানে কোনো cricket,
            # football বা ban filter নেই।

            match_entries = fetch_match_streams(
                event
            )


            if match_entries:

                all_entries.extend(
                    match_entries
                )

                print(
                    f"   ✅ Added "
                    f"{len(match_entries)} streams"
                )

            else:

                print(
                    "   ⚠️ No streams found"
                )


        # ----------------------------------
        # Bangladesh timestamp
        # ----------------------------------

        timestamp = (
            datetime.utcnow()
            + timedelta(hours=6)
        ).strftime(
            "%Y-%m-%d %I:%M %p BST"
        )


        # ----------------------------------
        # Create / Update playlist.m3u
        # ----------------------------------

        with open(
            "playlist.m3u",
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "#EXTM3U\n"
            )

            f.write(
                f"# UPDATED: "
                f"{timestamp}\n\n"
            )


            for entry in all_entries:

                f.write(
                    entry
                )


        # ----------------------------------
        # Final result
        # ----------------------------------

        print(
            "\n================================"
        )

        print(
            f"🎉 Playlist Updated!"
        )

        print(
            f"📺 Total streams: "
            f"{len(all_entries)}"
        )

        print(
            f"🕐 Updated: "
            f"{timestamp}"
        )

        print(
            "================================"
        )


    except Exception as e:

        print(
            f"❌ Error: {e}"
        )


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    main()
