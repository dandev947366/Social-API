import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
import googleapiclient.errors
import google_auth_httplib2

# Load environment variables from the .env file
load_dotenv()

# Get the YouTube API key from the environment variable
api_key = os.getenv('YOUTUBE_API_KEY')

# Check if the API key is loaded properly
if not api_key:
    raise ValueError("YouTube API key not found. Please check your .env file.")

# Build the YouTube service for retrieving video details (Read-Only access)
youtube = build('youtube', 'v3', developerKey=api_key)

# Define the video ID
video_id = 'NYz_rWFlTnM'

# Make a request to get video details
request = youtube.videos().list(
    part='snippet,contentDetails,statistics',
    id=video_id
)
response = request.execute()

# Extract and display relevant data
if 'items' in response and len(response['items']) > 0:
    video = response['items'][0]
    title = video['snippet']['title']
    description = video['snippet']['description']
    published_at = video['snippet']['publishedAt']
    view_count = video['statistics']['viewCount']
    like_count = video['statistics'].get('likeCount', 'N/A')
    comment_count = video['statistics'].get('commentCount', 'N/A')

    print(f"Title: {title}")
    print(f"Description: {description}")
    print(f"Published at: {published_at}")
    print(f"Views: {view_count}")
    print(f"Likes: {like_count}")
    print(f"Comments: {comment_count}")
else:
    print("No video found with the given ID.")

# OAuth 2.0 authentication function to post a comment
def get_authenticated_service():
    # Specify the scope for managing YouTube comments
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

    # Initialize the flow using client secrets file
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'credentials.json', scopes
    )
    credentials = flow.run_local_server(port=64040)

    # Build the authenticated YouTube client
    youtube_auth = build('youtube', 'v3', credentials=credentials)
    return youtube_auth

# Function to post a comment on the video
def post_comment(video_id, comment_text):
    youtube_auth = get_authenticated_service()

    # Construct the request to insert a comment
    request = youtube_auth.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
    )
    response = request.execute()
    print("Comment posted successfully!")
    print(f"Response: {response}")

# Replace with your desired comment
comment_text = "Hyva. Kiitos paljon!!"

# Post the comment
post_comment(video_id, comment_text)
