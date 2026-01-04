import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import re
import json

# Configuration
RSS_URL = "https://toolbox.leaflet.pub/rss"
POSTS_DIR = "content/posts"

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def sync():
    if not os.path.exists(POSTS_DIR):
        os.makedirs(POSTS_DIR)

    print(f"Fetching RSS feed from {RSS_URL}...")
    try:
        with urllib.request.urlopen(RSS_URL) as response:
            rss_data = response.read()
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return

    try:
        root = ET.fromstring(rss_data)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return

    items = root.findall(".//item")

    # Namespaces
    ns = {
        'content': 'http://purl.org/rss/1.0/modules/content/',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    for item in items:
        title = item.find("title").text
        link = item.find("link").text
        pub_date_str = item.find("pubDate").text
        description = item.find("description").text if item.find("description") is not None else ""
        
        # Extract content:encoded if available
        content_encoded = item.find("content:encoded", ns)
        content = content_encoded.text if content_encoded is not None else description

        # Parse date
        # Sun, 28 Dec 2025 11:51:32 GMT or similar
        try:
            pub_date = datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            try:
                # Fallback for different formats
                pub_date = datetime.strptime(pub_date_str[:25].strip(), "%a, %d %b %Y %H:%M:%S")
            except ValueError:
                print(f"Could not parse date: {pub_date_str}")
                continue

        date_iso = pub_date.strftime("%Y-%m-%d")
        slug = slugify(title)
        filename = f"{date_iso}-{slug}.md"
        filepath = os.path.join(POSTS_DIR, filename)

        if os.path.exists(filepath):
            # print(f"Post already exists: {filename}")
            continue

        print(f"Creating new post: {filename}")
        
        # Hugo front matter (JSON dumped for safety with quotes)
        safe_title = json.dumps(title)
        safe_description = json.json.dumps(description)
        
        front_matter = [
            "---",
            f'title: {safe_title}',
            f"date: {pub_date.isoformat()}Z",
            f'description: {safe_description}',
            "draft: false",
            "---",
            "",
            f"*Originally published at [Leaflet]({link})*",
            "",
            content
        ]

        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(front_matter))

    print("Sync complete.")

if __name__ == "__main__":
    sync()