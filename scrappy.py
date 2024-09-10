from flask import Flask, request, render_template, jsonify, session
import requests
from bs4 import BeautifulSoup
import time
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session handling

# List of User-Agents to rotate
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

def get_random_headers():
    """Generate random headers for each request."""
    headers = {
        "User-Agent": random.choice(user_agents),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    return headers

def fetch_lyrics(url, artist_name):
    """Fetch song lyrics and update progress, with random delays and headers."""
    try:
        print(f"Fetching lyrics from: {url}")
        response = requests.get(url, headers=get_random_headers())
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Handle different lyric sites
        if "azlyrics.com" in url:
            tables = soup.find_all("table", {"class": "table table-condensed"})
        elif "genius.com" in url:
            # Assuming Genius uses a 'lyrics' div
            tables = soup.find_all("div", {"class": "lyrics"})
        else:
            tables = None  # Handle other sites as needed

        table_data = []
        if tables:
            total_songs = len(tables)
            for i, table in enumerate(tables, start=1):
                rows = table.find_all("tr")
                for row in rows:
                    link = row.find("a")
                    if link:
                        song_title = link.text.strip()
                        song_url = link.get("href")
                        if song_url and song_url.startswith("/"):
                            song_url = f"https://www.azlyrics.com{song_url}"
                        lyrics = fetch_song_lyrics(song_url)
                        table_data.append([i, artist_name, song_title, song_url, lyrics])

                        # Simulate random delay to avoid detection as a bot
                        progress = int((i / total_songs) * 100)
                        session['progress'] = progress
                        delay = random.uniform(2, 5)  # Random delay between 2 and 5 seconds
                        print(f"Sleeping for {delay:.2f} seconds...")
                        time.sleep(delay)
        else:
            return "No lyrics found for this URL."

        return table_data

    except requests.RequestException as e:
        print(f"Error fetching lyrics page: {e}")
        return f"Error fetching data: {e}"

def fetch_song_lyrics(url):
    """Fetch the lyrics from the song URL."""
    try:
        print(f"Fetching song from URL: {url}")
        response = requests.get(url, headers=get_random_headers())
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # The lyrics are usually within a div after certain elements (ads, scripts, etc.)
        lyrics_div = soup.find("div", {"class": "col-xs-12 col-lg-8 text-center"})

        if lyrics_div:
            lyrics = lyrics_div.find_all("div")[6].get_text(strip=True)
            return lyrics
        return "Lyrics not found"

    except requests.RequestException as e:
        print(f"Error fetching lyrics: {e}")
        return "Error fetching lyrics"

@app.route('/progress')
def progress():
    """Endpoint to return progress."""
    return jsonify(progress=session.get('progress', 0))

@app.route('/', methods=['GET', 'POST'])
def index():
    lyrics_data = None
    error = None
    if request.method == 'POST':
        artist_name = request.form['artist_name'].strip().replace(" ", "+")
        custom_url = request.form.get('custom_url')

        # If a custom URL is provided, use it; otherwise, construct the Azlyrics search URL
        if custom_url and custom_url.strip():
            url = custom_url.strip()
        else:
            url = f"https://search.azlyrics.com/search.php?q={artist_name}&w=lyrics"

        lyrics_data = fetch_lyrics(url, artist_name)
        session['progress'] = 100  # Set to 100% once lyrics are fetched
    return render_template('index.html', lyrics_data=lyrics_data, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1990, debug=True)
