# Social Media Integration API (Reddit & YouTube) with Python Flask

This project provides a simple API for integrating with Reddit and YouTube using Python Flask. It allows you to fetch Reddit posts from the "all" subreddit and search for YouTube videos based on a query.

## Features
- **Reddit Integration**: Fetches the latest posts from the "all" subreddit.
- **YouTube Integration**: Searches for YouTube videos based on a provided query.
- **User Authentication**: Basic login functionality for access control.
- **Pagination**: Both Reddit and YouTube endpoints support pagination.

## Technologies Used
- Python 3
- Flask (Web Framework)
- PRAW (Python Reddit API Wrapper)
- Google API Client (for YouTube integration)
- dotenv (Environment Variable Management)
- Flask-CORS (Cross-Origin Resource Sharing support)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/social-media-integration-api.git
   cd social-media-integration-api
   ```

2. Set up a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory of the project and add the following environment variables:
   
   ```bash
   REDDIT_CLIENT_ID=your_reddit_client_id
   REDDIT_CLIENT_SECRET=your_reddit_client_secret
   REDDIT_USER_AGENT=your_reddit_user_agent
   YOUTUBE_API_KEY=your_youtube_api_key
   ```

5. Run the Flask app:

   ```bash
   python app.py
   ```

6. The app will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. `/api/reddit_posts`
Fetches the latest posts from the "all" subreddit.

- **GET Parameters**:
  - `after`: Optional parameter to paginate through the posts.
  
**Example request**:
```
GET /api/reddit_posts?after=t3_k2wq23
```

**Response**:
```json
{
  "posts": [
    {
      "id": "12345",
      "source": "Reddit",
      "title": "Sample Reddit Post",
      "score": 100,
      "url": "https://www.reddit.com/r/all/comments/12345/sample_reddit_post",
      "author": "username",
      "created": 1636548495,
      "num_comments": 5,
      "thumbnail": "https://thumbnail.jpg",
      "selftext": "This is a sample post...",
      "created_datetime": "2023-01-15T12:34:56Z"
    }
  ],
  "after": "t3_k2wq24"
}
```

### 2. `/api/youtube_videos`
Searches YouTube videos based on a query.

- **GET Parameters**:
  - `query`: Search term for YouTube videos.
  - `pageToken`: Optional parameter for pagination.

**Example request**:
```
GET /api/youtube_videos?query=python&pageToken=CAEQAA
```

**Response**:
```json
{
  "videos": [
    {
      "id": "abc123",
      "source": "YouTube",
      "title": "Python Tutorial",
      "description": "Learn Python from scratch.",
      "thumbnail": "https://image_url.jpg",
      "channelTitle": "Python Channel",
      "publishedAt": "2023-01-15T12:34:56Z",
      "url": "https://www.youtube.com/watch?v=abc123"
    }
  ],
  "nextPageToken": "CAEQAA"
}
```

### 3. `/login`
Login page for accessing the main dashboard.

- **POST Parameters**:
  - `username`: Username of the user.
  - `password`: Password for the user.

**Example request**:
```
POST /login
```

**Response**:
Redirects to `/index` upon successful login.

## Environment Variables
The project relies on the following environment variables for API credentials and configuration:

- **REDDIT_CLIENT_ID**: Your Reddit application client ID.
- **REDDIT_CLIENT_SECRET**: Your Reddit application client secret.
- **REDDIT_USER_AGENT**: A custom user agent string for Reddit API requests.
- **YOUTUBE_API_KEY**: Your YouTube Data API key.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PRAW Documentation](https://praw.readthedocs.io/)
- [Google API Client Documentation](https://developers.google.com/api-client-library/python)

---
