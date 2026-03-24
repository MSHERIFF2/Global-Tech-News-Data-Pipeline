import requests
import json

def extract_tech_news(**kwargs):
    # 1. Get top story IDs
    top_ids_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    top_ids = requests.get(top_ids_url).json()[:20] 
    
    stories = []
    for s_id in top_ids:
        item_url = f"https://hacker-news.firebaseio.com/v0/item/{s_id}.json"
        stories.append(requests.get(item_url).json())
    
    # Save to XCom or a temporary local file in the container
    raw_path = "/tmp/raw_news.json"
    with open(raw_path, 'w') as f:
        json.dump(stories, f)
    return raw_path