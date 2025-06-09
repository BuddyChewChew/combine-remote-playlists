import requests
from datetime import datetime
import re

# Playlist URLs to combine
playlists = [
    "https://raw.githubusercontent.com/BuddyChewChew/My-Streams/refs/heads/main/Backup.m3u",
    "https://tinyurl.com/drewall8",
    "https://cdn.djdoolky76.net/udptv.m3u"
]

# Combined EPG URL
epg_url = "https://epgshare01.online/epgshare01/epg_ripper_ALL_SOURCES1.xml.gz"

# Output file
output_file = "combined_playlist.m3u"

def fetch_and_combine_playlists():
    with open(output_file, "w", encoding="utf-8") as outfile:
        # Write header with EPG URL
        outfile.write(f'#EXTM3U x-tvg-url="{epg_url}"\n\n')
        outfile.write(f'# Generated on {datetime.utcnow().isoformat()} UTC\n\n')  # Add timestamp
        
        for url in playlists:
            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                lines = response.text.splitlines()

                # Add 📺 source comment before the channels
                outfile.write(f'# 📺 Source: {url}\n')

                for line in lines:
                    if not line.startswith("#EXTM3U"):  # Skip the initial header
                        # Remove group-title="" tags
                        line = re.sub(r'group-title="[^"]*"', '', line)
                        outfile.write(line + "\n")

                outfile.write("\n")  # Space between sources
                print(f"✅ Added channels from {url}")

            except Exception as e:
                print(f"❌ Failed to fetch {url}: {e}")

    print(f"\n✅ Combined playlist saved as '{output_file}' with EPG: {epg_url}")

if __name__ == "__main__":
    fetch_and_combine_playlists()
