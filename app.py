

from flask import Flask, render_template, jsonify, request, redirect, url_for
import os
from dotenv import load_dotenv
import datetime
from flask_cors import CORS
import praw
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = Flask(__name__, static_folder='static') 
CORS(app)
load_dotenv()

# Reddit API credentials from environment variables
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'my_reddit_app')

# YouTube API key from environment variables
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Setting up PRAW (Python Reddit API Wrapper)
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT,
    check_for_async=False
)

# Function to get YouTube videos
def get_youtube_videos(query=None, page_token=None):
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

        search_params = {
            'part': 'snippet',
            'type': 'video',
            'maxResults': 5,
            'order': 'date',
        }

        if query:
            search_params['q'] = query

        if page_token:
            search_params['pageToken'] = page_token

        search_response = youtube.search().list(**search_params).execute()

        videos = []
        for item in search_response.get('items', []):
            video_data = {
                'id': item['id']['videoId'],
                'source': 'YouTube',
                'title': item['snippet']['title'],
                'description': item['snippet']['description'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'],
                'channelTitle': item['snippet']['channelTitle'],
                'publishedAt': item['snippet']['publishedAt'],
                'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            }
            videos.append(video_data)

        next_page_token = search_response.get('nextPageToken')

        return {'videos': videos, 'nextPageToken': next_page_token}

    except HttpError as e:
        print(f"An HTTP error occurred: {e}")
        return {'videos': [], 'nextPageToken': None}


@app.route('/')
def main():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == "Hatem" and password == "12345":  
            return redirect(url_for('home'))
        elif username == "Alaa" and password == "12345": 
            return redirect(url_for('home'))
        elif username == "Mostafa" and password == "12345": 
            return redirect(url_for('home'))
        else:
            return "Login Failed", 401
    return render_template('loginPage.html')

@app.route('/index')
def home():
    return render_template('index.html')

# Reddit Posts API Endpoint
@app.route('/api/reddit_posts')
def get_reddit_posts():
    try:
        posts = []
        subreddit = reddit.subreddit('all')

        limit = 5  # Number of posts to fetch per request
        after = request.args.get('after')  # Get the 'after' parameter from the query string

        # Fetch posts with or without the 'after' parameter
        if after:
            submissions = subreddit.new(limit=limit, params={'after': after})
        else:
            submissions = subreddit.new(limit=limit)

        last_post_fullname = None

        for post in submissions:
            last_post_fullname = post.fullname  # Save the fullname of the last post for pagination

            posts.append({
                'id': post.id,
                'source': 'Reddit',
                'title': post.title,
                'score': post.score,
                'url': post.url,
                'author': post.author.name if post.author else 'N/A',
                'created': post.created_utc,
                'num_comments': post.num_comments,
                'thumbnail': post.thumbnail if post.thumbnail.startswith('http') else None,
                'selftext': post.selftext[:300] + '...' if len(post.selftext) > 300 else post.selftext,
                'created_datetime': datetime.datetime.utcfromtimestamp(post.created_utc).isoformat() + 'Z'
            })

        # Return the posts along with the 'after' value for the next request
        return jsonify({'posts': posts, 'after': last_post_fullname})
    except Exception as e:
        # Log the error and return an empty list
        print(f"Error fetching Reddit posts: {e}")
        return jsonify({'posts': [], 'after': None})

# YouTube Videos API Endpoint
@app.route('/api/youtube_videos')
def youtube_videos():
    query = request.args.get('query')
    page_token = request.args.get('pageToken')

    data = get_youtube_videos(query=query, page_token=page_token)
    return jsonify(data)

if __name__ == '__main__':
    # Debugging: List all routes
    print('Registered routes:')
    for rule in app.url_map.iter_rules():
        print(f'{rule}')

    app.run(debug=True)
    
    
#python3 app.py
