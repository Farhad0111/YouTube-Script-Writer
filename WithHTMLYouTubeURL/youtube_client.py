import os
import json
from typing import Dict, Any, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

class YouTubeClient:
    def __init__(self):
        self._service = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    def extract_channel_id(self, input_text: str) -> str:
        """
        Extract the channel ID from various YouTube channel URL formats or return the ID directly.
        
        Handles formats like:
        - https://www.youtube.com/channel/UC1234567890
        - https://www.youtube.com/c/ChannelName
        - https://www.youtube.com/@username
        - UC1234567890 (direct ID)
        """
        input_text = input_text.strip()
        
        # If it's already a channel ID (starts with UC)
        if input_text.startswith('UC') and len(input_text) > 10:
            return input_text
            
        # Extract from /channel/ URL
        if '/channel/' in input_text:
            parts = input_text.split('/channel/')
            if len(parts) > 1:
                return parts[1].split('/')[0].split('?')[0]
        
        # Handle /c/ or /user/ or @username formats by retrieving channel info
        try:
            if '/c/' in input_text or '/user/' in input_text or '@' in input_text:
                # Extract the username part
                username = None
                if '/c/' in input_text:
                    username = input_text.split('/c/')[1].split('/')[0].split('?')[0]
                elif '/user/' in input_text:
                    username = input_text.split('/user/')[1].split('/')[0].split('?')[0]
                elif '@' in input_text:
                    if '/@' in input_text:
                        username = input_text.split('/@')[1].split('/')[0].split('?')[0]
                    else:
                        username = input_text.replace('@', '')
                
                if username:
                    # Search for the channel
                    search_response = self._service.search().list(
                        q=username,
                        type='channel',
                        part='snippet',
                        maxResults=1
                    ).execute()
                    
                    if search_response.get('items'):
                        return search_response['items'][0]['snippet']['channelId']
        except HttpError:
            # Fall back to using the input as is if we can't resolve it
            pass
            
        # Return original if we couldn't extract anything
        return input_text
    
    def get_channel_info(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """Get channel details including title, description, stats"""
        try:
            channel_id = self.extract_channel_id(channel_id)
            
            # Get basic channel info
            channel_response = self._service.channels().list(
                part='snippet,statistics,brandingSettings',
                id=channel_id
            ).execute()
            
            if not channel_response.get('items'):
                return None
                
            channel_data = channel_response['items'][0]
            
            # Get recent videos to analyze content
            videos_response = self._service.search().list(
                channelId=channel_id,
                part='snippet',
                order='date',
                type='video',
                maxResults=10
            ).execute()
            
            videos = []
            for item in videos_response.get('items', []):
                video_id = item['id']['videoId']
                
                # Get video details including title, description
                video_response = self._service.videos().list(
                    part='snippet,statistics',
                    id=video_id
                ).execute()
                
                if video_response.get('items'):
                    video_data = video_response['items'][0]
                    videos.append({
                        'id': video_id,
                        'title': video_data['snippet']['title'],
                        'description': video_data['snippet']['description'],
                        'views': video_data['statistics'].get('viewCount', 0),
                        'likes': video_data['statistics'].get('likeCount', 0),
                        'comments': video_data['statistics'].get('commentCount', 0)
                    })
            
            # Compile full channel data
            return {
                'id': channel_id,
                'title': channel_data['snippet']['title'],
                'description': channel_data['snippet']['description'],
                'customUrl': channel_data['snippet'].get('customUrl', ''),
                'publishedAt': channel_data['snippet']['publishedAt'],
                'viewCount': channel_data['statistics'].get('viewCount', 0),
                'subscriberCount': channel_data['statistics'].get('subscriberCount', 0),
                'videoCount': channel_data['statistics'].get('videoCount', 0),
                'keywords': channel_data.get('brandingSettings', {}).get('channel', {}).get('keywords', ''),
                'videos': videos
            }
        except HttpError as e:
            print(f"YouTube API error: {str(e)}")
            return None
        except Exception as e:
            print(f"Error getting channel info: {str(e)}")
            return None