from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime

# Replace with your YouTube API Key
API_KEY = "AIzaSyBuLFe_AiMD5jIat6Y_FWvFTRmFV59QGYs"

# Set up YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

# Function to get category names
def get_video_categories(region_code="IN"):
    request = youtube.videoCategories().list(
        part="snippet",
        regionCode=region_code
    )
    response = request.execute()

    category_mapping = {item["id"]: item["snippet"]["title"] for item in response["items"]}
    return category_mapping

# Function to get channel details
def get_channel_details(channel_id):
    request = youtube.channels().list(
        part="snippet",
        id=channel_id
    )
    response = request.execute()

    # Get channel profile picture URL
    channel_data = response["items"][0]["snippet"]
    profile_picture_url = channel_data["thumbnails"]["default"]["url"]  # Default thumbnail size
    return profile_picture_url

# Function to get trending videos
def get_trending_videos(region_code="IN", max_results=20):  # Update max_results to 20
    category_mapping = get_video_categories(region_code)
    
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=max_results  # Fetch 20 videos
    )
    response = request.execute()

    trending_videos = []
    today_date = datetime.today().strftime('%Y-%m-%d')  # Trending Date

    for rank, video in enumerate(response["items"], start=1):
        channel_id = video["snippet"]["channelId"]
        profile_picture_url = get_channel_details(channel_id)  # Get channel profile picture
        
        video_data = {
            "Rank": f"#{rank}",
            "Title": video["snippet"]["title"],
            "Channel": video["snippet"]["channelTitle"],
            "Channel Profile Picture": profile_picture_url,  # Add profile picture URL
            "Views": int(video["statistics"].get("viewCount", 0)),
            "Likes": int(video["statistics"].get("likeCount", 0)) if "likeCount" in video["statistics"] else "N/A",
            "Category": category_mapping.get(video["snippet"]["categoryId"], "Unknown"),
            "Trending Date": today_date,
            "Video URL": f"https://www.youtube.com/watch?v={video['id']}",
            "Country" : f"India"
        }
        trending_videos.append(video_data)

    return trending_videos

# Fetch trending videos for the US
trending_videos = get_trending_videos(region_code="IN", max_results=20)  # Request 20 trending videos

# Convert to DataFrame and display
df = pd.DataFrame(trending_videos)
print(df)

# Save to CSV
df.to_csv("YouTube_Trending_Videos_India.csv", index=False)
