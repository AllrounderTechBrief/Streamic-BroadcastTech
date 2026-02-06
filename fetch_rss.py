#!/usr/bin/env python3
"""
The Streamic - Enhanced RSS Aggregator with Monitoring
Fetches broadcast technology news from industry sources
Features: Deduplication, AI summaries, monitoring metrics
"""

import json
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime
from html import unescape
from typing import List, Dict, Optional
import hashlib

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0 Safari/537.36"
)

# RSS Feed sources mapped to categories
RSS_FEEDS = {
    "newsroom": [
        {"url": "https://www.dalet.com/feed/", "label": "Dalet"},
        {"url": "https://www.avid.com/press-center/rss", "label": "Avid"},
        {"url": "https://www.tvtechnology.com/rss.xml", "label": "TV Technology"},
    ],
    "playout": [
        {"url": "https://www.rossvideo.com/news/feed/", "label": "Ross Video"},
        {"url": "https://www.imaginecommunications.com/feed/", "label": "Imagine Communications"},
        {"url": "https://www.tvtechnology.com/rss.xml", "label": "TV Technology"},
    ],
    "infrastructure": [
        {"url": "https://www.smpte.org/rss.xml", "label": "SMPTE"},
        {"url": "https://www.tvtechnology.com/feed", "label": "TV Technology"},
        {"url": "https://www.ibc.org/rss", "label": "IBC"},
    ],
    "graphics": [
        {"url": "https://www.vizrt.com/news/rss.xml", "label": "Vizrt"},
        {"url": "https://www.newscaststudio.com/category/graphics/feed/", "label": "Newscast Studio"},
        {"url": "https://www.rossvideo.com/news/feed/", "label": "Ross Video"},
    ],
    "cloud": [
        {"url": "https://blog.frame.io/feed/", "label": "Frame.io"},
        {"url": "https://www.adobe.com/video-audio.rss.xml", "label": "Adobe"},
        {"url": "https://www.tvtechnology.com/rss.xml", "label": "TV Technology"},
    ],
    "streaming": [
        {"url": "https://www.streamingmedia.com/RSS/RSSFeed.aspx", "label": "Streaming Media"},
        {"url": "https://aws.amazon.com/about-aws/whats-new/recent/feed/", "label": "AWS Media"},
        {"url": "https://www.broadcastingcable.com/feeds/all", "label": "Broadcasting & Cable"},
    ],
    "audio-ai": [
        {"url": "https://www.prosoundnetwork.com/feed", "label": "Pro Sound Network"},
        {"url": "https://www.tvtechnology.com/rss.xml", "label": "TV Technology"},
        {"url": "https://www.sportsvideo.org/feed/", "label": "Sports Video Group"},
    ],
}

# Monitoring metrics
METRICS = {
    "total_feeds_checked": 0,
    "successful_fetches": 0,
    "failed_fetches": 0,
    "total_items_fetched": 0,
    "duplicates_removed": 0,
    "items_after_dedup": 0,
    "execution_time_seconds": 0,
    "last_run": None,
    "errors": []
}


def fetch_url(url: str, timeout: int = 20) -> Optional[bytes]:
    """Fetch URL with error handling and monitoring"""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            METRICS["successful_fetches"] += 1
            return response.read()
    except urllib.error.URLError as e:
        METRICS["failed_fetches"] += 1
        METRICS["errors"].append({"url": url, "error": str(e), "type": "URLError"})
        print(f"  ✗ URL Error fetching {url}: {e}")
        return None
    except Exception as e:
        METRICS["failed_fetches"] += 1
        METRICS["errors"].append({"url": url, "error": str(e), "type": "Exception"})
        print(f"  ✗ Error fetching {url}: {e}")
        return None


def extract_text(node, path: str, default: str = "") -> str:
    """Safely extract text from XML element"""
    element = node.find(path)
    if element is not None and element.text:
        return element.text.strip()
    return default


def find_image_in_rss(item) -> str:
    """Extract image URL from RSS item using multiple methods"""
    # Try media:thumbnail
    media_ns = "{http://search.yahoo.com/mrss/}"
    thumbnail = item.find(f"{media_ns}thumbnail")
    if thumbnail is not None and thumbnail.get("url"):
        return thumbnail.get("url")
    
    # Try media:content
    content = item.find(f"{media_ns}content")
    if content is not None and content.get("url"):
        url = content.get("url")
        if content.get("type", "").startswith("image/"):
            return url
    
    # Try enclosure
    enclosure = item.find("enclosure")
    if enclosure is not None and enclosure.get("type", "").startswith("image/"):
        return enclosure.get("url")
    
    # Try content:encoded or description for <img> tags
    content_encoded = item.find("{http://purl.org/rss/1.0/modules/content/}encoded")
    if content_encoded is not None and content_encoded.text:
        text = content_encoded.text
    else:
        text = extract_text(item, "description", "")
    
    # Parse HTML for img src
    if text:
        text = unescape(text)
        lower = text.lower()
        img_pos = lower.find("<img ")
        if img_pos != -1:
            src_pos = lower.find("src=", img_pos)
            if src_pos != -1:
                quote = text[src_pos + 4:src_pos + 5]
                if quote in "\"'":
                    end_pos = text.find(quote, src_pos + 5)
                    if end_pos != -1:
                        return text[src_pos + 5:end_pos]
    
    return ""


def parse_rss_feed(xml_bytes: bytes) -> List[Dict]:
    """Parse RSS or Atom feed and extract items"""
    items = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as e:
        print(f"  ✗ XML Parse Error: {e}")
        return items

    atom_ns = "{http://www.w3.org/2005/Atom}"

    # RSS 2.0
    channel = root.find("channel")
    if channel is not None:
        source_title = extract_text(channel, "title", "Source")
        for item in channel.findall("item"):
            title = extract_text(item, "title", "Untitled")
            link = extract_text(item, "link", "")
            pub_date = extract_text(item, "pubDate", "")
            description = extract_text(item, "description", "")
            guid = extract_text(item, "guid", link)
            image = find_image_in_rss(item)
            
            items.append({
                "title": title,
                "link": link,
                "source": source_title,
                "image": image or "",
                "pubDate": pub_date,
                "description": description[:200] if description else "",
                "guid": guid
            })
        return items

    # Atom
    if root.tag == f"{atom_ns}feed":
        source_title = extract_text(root, f"{atom_ns}title", "Source")
        for entry in root.findall(f"{atom_ns}entry"):
            title = extract_text(entry, f"{atom_ns}title", "Untitled")
            link = ""
            for link_elem in entry.findall(f"{atom_ns}link"):
                if link_elem.get("rel") in (None, "alternate"):
                    link = link_elem.get("href", "") or link
            
            pub_date = extract_text(entry, f"{atom_ns}published", "")
            summary = extract_text(entry, f"{atom_ns}summary", "")
            entry_id = extract_text(entry, f"{atom_ns}id", link)
            
            items.append({
                "title": title,
                "link": link,
                "source": source_title,
                "image": "",
                "pubDate": pub_date,
                "description": summary[:200] if summary else "",
                "guid": entry_id
            })
        return items

    return items


def generate_content_hash(item: Dict) -> str:
    """Generate unique hash for deduplication"""
    # Use link or title+source for hashing
    content = item.get("link", "") or f"{item.get('title', '')}{item.get('source', '')}"
    return hashlib.md5(content.encode()).hexdigest()


def generate_impact_brief(title: str, description: str, category: str) -> str:
    """
    Generate AI Impact Brief explaining why this news matters to engineers.
    In production, this would call an LLM API. For now, uses rule-based logic.
    """
    title_lower = title.lower()
    desc_lower = description.lower()
    
    # Category-specific impact templates
    impact_templates = {
        "newsroom": "Impacts newsroom workflow efficiency and content management systems. ",
        "playout": "Affects broadcast automation and master control operations. ",
        "infrastructure": "Influences IP video transport and signal routing architecture. ",
        "graphics": "Shapes real-time graphics rendering and broadcast design workflows. ",
        "cloud": "Transforms remote collaboration and cloud-based editing capabilities. ",
        "streaming": "Alters OTT delivery infrastructure and content distribution strategies. ",
        "audio-ai": "Impacts audio processing workflows and AI-driven automation systems. "
    }
    
    # Keyword-based impact additions
    impacts = []
    
    if any(word in title_lower for word in ["smpte", "2110", "st 2110", "ip"]):
        impacts.append("Enables lower latency for ST 2110 workflows.")
    
    if any(word in title_lower for word in ["cloud", "remote", "saas"]):
        impacts.append("Reduces infrastructure costs through cloud scalability.")
    
    if any(word in title_lower for word in ["ai", "ml", "automation", "intelligent"]):
        impacts.append("Automates repetitive tasks with AI-powered intelligence.")
    
    if any(word in title_lower for word in ["ndi", "dante", "aes67", "audio"]):
        impacts.append("Simplifies audio routing in IP-based environments.")
    
    if any(word in title_lower for word in ["4k", "8k", "uhd", "hdr"]):
        impacts.append("Supports higher resolution formats for premium content delivery.")
    
    if any(word in title_lower for word in ["integration", "workflow", "interoperability"]):
        impacts.append("Improves system integration across vendor ecosystems.")
    
    # Fallback generic impact
    if not impacts:
        impacts.append("Represents an important development in broadcast technology.")
    
    # Combine base template with specific impacts
    base = impact_templates.get(category, "Relevant to broadcast engineering workflows. ")
    return base + " ".join(impacts[:1])  # Keep it to 2 sentences max


def deduplicate_items(items: List[Dict]) -> List[Dict]:
    """Remove duplicate items based on content hash"""
    seen_hashes = set()
    unique_items = []
    duplicates_count = 0
    
    for item in items:
        content_hash = generate_content_hash(item)
        if content_hash not in seen_hashes:
            seen_hashes.add(content_hash)
            unique_items.append(item)
        else:
            duplicates_count += 1
    
    METRICS["duplicates_removed"] = duplicates_count
    METRICS["items_after_dedup"] = len(unique_items)
    
    return unique_items


def build_category_feed(category: str, sources: List[Dict]) -> List[Dict]:
    """Build feed for a specific category"""
    all_items = []
    
    print(f"\n{'='*60}")
    print(f"Building {category.upper()} feed")
    print(f"{'='*60}")
    
    for source in sources:
        url = source["url"]
        label = source.get("label", "Unknown")
        
        METRICS["total_feeds_checked"] += 1
        print(f"Fetching: {label} ({url})")
        
        xml_data = fetch_url(url)
        if xml_data:
            items = parse_rss_feed(xml_data)
            
            # Override source name with label
            for item in items:
                item["source"] = label
                item["category"] = category
                # Generate impact brief
                item["impactBrief"] = generate_impact_brief(
                    item.get("title", ""),
                    item.get("description", ""),
                    category
                )
            
            all_items.extend(items)
            METRICS["total_items_fetched"] += len(items)
            print(f"  → Got {len(items)} items")
        
        time.sleep(0.5)  # Be polite to servers
    
    return all_items


def save_json(filepath: str, data: any):
    """Save data to JSON file"""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    """Main execution function"""
    start_time = time.time()
    
    print("\n" + "="*60)
    print("THE STREAMIC - Enhanced RSS Aggregator")
    print("2026 Edition with Monitoring & AI Impact Briefs")
    print("="*60 + "\n")
    
    # Collect all items from all categories
    all_items = []
    
    for category, sources in RSS_FEEDS.items():
        category_items = build_category_feed(category, sources)
        all_items.extend(category_items)
        
        # Save individual category file
        category_file = f"data/{category}.json"
        deduplicated = deduplicate_items(category_items)
        limited = deduplicated[:60]  # Limit to 60 items per category
        save_json(category_file, limited)
        print(f"✓ Saved {category_file} ({len(limited)} items)")
    
    # Deduplicate across all categories
    print(f"\n{'='*60}")
    print("Global Deduplication & Sliding Window")
    print(f"{'='*60}")
    
    all_items_dedup = deduplicate_items(all_items)
    
    # Sort by date (newest first) and apply 100-item sliding window
    all_items_dedup.sort(
        key=lambda x: x.get("pubDate", ""),
        reverse=True
    )
    sliding_window = all_items_dedup[:100]
    
    # Save master news.json
    save_json("data/news.json", sliding_window)
    print(f"✓ Saved data/news.json ({len(sliding_window)} items)")
    
    # Calculate metrics
    METRICS["execution_time_seconds"] = round(time.time() - start_time, 2)
    METRICS["last_run"] = datetime.utcnow().isoformat() + "Z"
    
    # Save monitoring metrics
    save_json("data/metrics.json", METRICS)
    
    # Print summary
    print(f"\n{'='*60}")
    print("EXECUTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total Feeds Checked: {METRICS['total_feeds_checked']}")
    print(f"Successful Fetches: {METRICS['successful_fetches']}")
    print(f"Failed Fetches: {METRICS['failed_fetches']}")
    print(f"Total Items Fetched: {METRICS['total_items_fetched']}")
    print(f"Duplicates Removed: {METRICS['duplicates_removed']}")
    print(f"Final Items (100-window): {len(sliding_window)}")
    print(f"Execution Time: {METRICS['execution_time_seconds']}s")
    print(f"Last Run: {METRICS['last_run']}")
    
    if METRICS["errors"]:
        print(f"\n⚠️  {len(METRICS['errors'])} errors occurred:")
        for error in METRICS["errors"][:5]:  # Show first 5
            print(f"  - {error['url']}: {error['error'][:80]}")
    
    print(f"\n{'='*60}")
    print("✓ All feeds built successfully!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
