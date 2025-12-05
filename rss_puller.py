import feedparser
import requests
from pipeline import yt_pipeline

from prefect import flow

def fetch_youtube_rss(channel_id):
    """
    Fetch and parse YouTube RSS feed for a given channel ID
    """
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the RSS feed
        feed = feedparser.parse(response.content)
        
        return feed
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching RSS feed: {e}")
        return None

def print_feed_info(feed):
    """
    Print parsed RSS feed information
    """
    if not feed:
        print("No feed data to display")
        return
    
    print(f"\n{'='*80}")
    print(f"Channel: {feed.feed.get('title', 'Unknown')}")
    print(f"Link: {feed.feed.get('link', 'Unknown')}")
    print(f"Total entries: {len(feed.entries)}")
    print(f"{'='*80}\n")
    
    for i, entry in enumerate(feed.entries, 1):
        print(f"\n--- Video {i} ---")
        print(f"Title: {entry.get('title', 'N/A')}")
        print(f"Video ID: {entry.get('yt_videoid', 'N/A')}")
        print(f"Link: {entry.get('link', 'N/A')}")
        print(f"Published: {entry.get('published', 'N/A')}")
        print(f"Author: {entry.get('author', 'N/A')}")
        
        # Media thumbnail if available
        if 'media_thumbnail' in entry:
            print(f"Thumbnail: {entry.media_thumbnail[0]['url']}")
        
        # Description
        if 'summary' in entry:
            summary = entry.summary[:200] + "..." if len(entry.summary) > 200 else entry.summary
            print(f"Description: {summary}")
        
        print("-" * 80)

def process_feed_videos(feed):
    """
    Extract video links from feed and pass them to the pipeline
    """
    if not feed or not feed.entries:
        print("No videos to process")
        return
    
    video_links = []
    
    for entry in feed.entries:
        link = entry.get('link')
        if link:
            video_links.append(link)
            print(f"Processing: {entry.get('title', 'Unknown')} - {link}")
    
    print(f"\nTotal videos found: {len(video_links)}\n")
    
    # Process each video through the pipeline
    for link in video_links:
        try:
            print(f"\n{'='*80}")
            print(f"Starting pipeline for: {link}")
            print(f"{'='*80}\n")
            yt_pipeline(url=link)
        except Exception as e:
            print(f"Error processing {link}: {e}")
            continue

@flow(name="YouTube Video to Summary Pipeline", log_prints=True)
def pull():
    # List of YouTube channel IDs
    channel_ids = [
        "UCXbKJML9pVclFHLFzpvBgWw",  # Markets by Zerodha
    ]
    
    for channel_id in channel_ids:
        print(f"\n{'#'*80}")
        print(f"Fetching RSS feed for channel: {channel_id}")
        print(f"{'#'*80}")
        
        feed = fetch_youtube_rss(channel_id)
        
        if feed:
            print_feed_info(feed)
            
            # Process the videos through the pipeline
            process_feed_videos(feed)
