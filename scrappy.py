from flask import Flask, request, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import random
import time

app = Flask(__name__)

progress = 0  # Global variable to track progress

def fetch_lyrics(url, artist_name):
    """Fetch song titles and lyrics with random delays and track progress."""
    try:
        global progress
        progress = 0  # Reset progress at the start
        
        print(f"Fetching lyrics from: {url}")
        response = requests.get(url)
        
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table", {"class": "table table-condensed"})
        
        table_data = []
        total_songs = len(tables) * 10  # Assuming 10 songs per table for simplicity
        current_count = 0
        
        for i, table in enumerate(tables, start=1):
            rows = table.find_all("tr")
            for row in rows:
                link = row.find("a")
                if link:
                    song_title = link.text.strip()
                    song_url = link.get("href")
                    if song_url:
                        if song_url.startswith("/"):
                            song_url = f"https://www.azlyrics.com{song_url}"
                        lyrics = fetch_song_lyrics(song_url)
                        table_data.append([i, artist_name, song_title, song_url, lyrics])
                        
                        # Update progress
                        current_count += 1
                        progress = int((current_count / total_songs) * 100)
                        
                        # Add a random delay between fetching each song's lyrics
                        time.sleep(random.uniform(2, 5))  
        
        progress = 100  # Mark progress as complete
        return table_data
    except requests.RequestException as e:
        return f"Error fetching data: {e}"

def fetch_song_lyrics(song_url):
    """Fetch song lyrics from the song's URL."""
    try:
        response = requests.get(song_url)
        time.sleep(random.uniform(2, 5))  # Random delay to avoid being blocked
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        lyrics_div = soup.find("div", class_=False, id=False)  # Assuming this fetches the correct lyrics div
        lyrics = lyrics_div.get_text(separator="\n").strip() if lyrics_div else "Lyrics not found"
        
        return lyrics
    except requests.RequestException as e:
        return f"Error fetching lyrics: {e}"

@app.route('/progress')
def get_progress():
    """Endpoint to get the progress."""
    global progress
    return jsonify({'progress': progress})

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist_name = request.form['artist_name'].strip().replace(" ", "+")
        url = f"https://search.azlyrics.com/search.php?q={artist_name}&w=lyrics&p=1&x=..."
        lyrics_data = fetch_lyrics(url, artist_name)
        return render_template('index.html', lyrics_data=lyrics_data)
    return render_template('index.html')

@app.route('/exit')
def exit():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1990, debug=True)
