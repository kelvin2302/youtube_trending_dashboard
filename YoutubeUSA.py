from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime


API_KEY = "AIzaSyBuLFe_AiMD5jIat6Y_FWvFTRmFV59QGYs"


youtube = build("youtube", "v3", developerKey=API_KEY)

def get_video_categories(region_code="US"):
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode=region_code
    )
    response = request.execute()

    category_mapping = {item["id"]: item["snippet"]["title"] for item in response["items"]}
    return category_mapping


def get_channel_details(channel_id):
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )
    response = request.execute()

  
    channel_data = response["items"][0]["snippet"]
    profile_picture_url = channel_data["thumbnails"]["default"]["url"]  
    return profile_picture_url


def get_trending_videos(region_code="US", max_results=20):  
    category_mapping = get_video_categories(region_code)
    
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results  
    )
    response = request.execute()

    trending_videos = []
    today_date = datetime.today().strftime('%Y-%m-%d') 

    for rank, video in enumerate(response["items"], start=1):
        channel_id = video["snippet"]["channelId"]
        profile_picture_url = get_channel_details(channel_id) 
        
        video_data = {
            "Rank": f"#{rank}",
            "Title": video["snippet"]["title"],
            "Channel": video["snippet"]["channelTitle"],
            "Channel Profile Picture": profile_picture_url,  
            "Views": int(video["statistics"].get("viewCount", 0)),
            "Likes": int(video["statistics"].get("likeCount", 0)) if "likeCount" in video["statistics"] else "N/A",
            "Category": category_mapping.get(video["snippet"]["categoryId"], "Unknown"),
            "Trending Date": today_date,
            "Video URL": f"https://www.youtube.com/watch?v={video['id']}",
            "Country" : f"USA"
        }
        trending_videos.append(video_data)

    return trending_videos


trending_videos = get_trending_videos(region_code="US", max_results=20)  

df = pd.DataFrame(trending_videos)
print(df)
df.to_csv("YouTube_Trending_Videos_USA.csv", index=False)
