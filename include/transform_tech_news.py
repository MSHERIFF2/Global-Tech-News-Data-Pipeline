import json
import pandas as pd

def transform_tech_news(**kwargs):
    ti = kwargs['ti']
    raw_path = ti.xcom_pull(task_ids='extract_data')
    
    with open(raw_path, 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data)
    df = df[['title', 'by', 'score', 'url', 'time']]
    df.rename(columns={'by': 'author', 'time': 'created_time'}, inplace=True)
    df['created_time'] = pd.to_datetime(df['created_time'], unit='s')
    
    # Bonus: Category Tagging
    def tag_category(title):
        t = str(title).upper()
        if 'AI' in t or 'LLM' in t: return 'AI'
        if 'CLOUD' in t or 'AWS' in t: return 'Cloud'
        if 'STARTUP' in t: return 'Startup'
        return 'General Tech'
    
    df['category'] = df['title'].apply(tag_category)
    
    # Bonus: Trending Insight (Logs)
    top_story = df.loc[df['score'].idxmax()]
    print(f"HIGHEST SCORE: {top_story['title']} ({top_story['score']} pts)")
    
    clean_path = "/tmp/tech_news.csv"
    df.to_csv(clean_path, index=False)
    return clean_path