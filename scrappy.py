from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def fetch_lyrics(url, artist_name):
    """Fetch song lyrics from the provided URL."""
    try:
        print(f"Fetching lyrics from: {url}")  # Debugging log
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        soup = BeautifulSoup(response.content, "html.parser")
        tables = soup.find_all("table", {"class": "table table-condensed"})
        
        table_data = []
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
                        print(f"Fetching lyrics for: {song_title}")
                        lyrics = fetch_song_lyrics(song_url)  # Fetch lyrics for each song
                        print(f"Lyrics fetched: {lyrics[:100]}")  # Debug: first 100 characters of lyrics
                        table_data.append([i, artist_name, song_title, song_url, lyrics])
        print(f"Fetched {len(table_data)} songs for artist: {artist_name}")  # Debug
        return table_data
    
    except requests.RequestException as e:
        print(f"Error fetching lyrics page: {e}")
        return f"Error fetching data: {e}"

def fetch_song_lyrics(url):
    """Fetch the lyrics from the song URL."""
    try:
        print(f"Fetching song from URL: {url}")  # Debugging log
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        soup = BeautifulSoup(response.content, "html.parser")
        
        # The lyrics are usually within a div after certain elements (ads, scripts, etc.)
        lyrics_div = soup.find("div", {"class": "col-xs-12 col-lg-8 text-center"})
        
        if lyrics_div:
            # Find the correct div which contains the lyrics
            lyrics = lyrics_div.find_all("div")[6].get_text(strip=True)  # Lyrics content
            return lyrics
        
        return "Lyrics not found"
    
    except requests.RequestException as e:
        print(f"Error fetching lyrics: {e}")
        return "Error fetching lyrics"

@app.route('/', methods=['GET', 'POST'])
def index():
    lyrics_data = None
    error = None
    if request.method == 'POST':
        artist_name = request.form['artist_name'].strip().replace(" ", "+")
        url = f"https://search.azlyrics.com/search.php?q={artist_name}&w=lyrics&p=1&x=7212ca797bf201758b9641f763c67f2c88a4bc8f3ce6c933097b8401e6ca9453"
        print(f"Searching for artist: {artist_name}")  # Debugging log
        lyrics_data = fetch_lyrics(url, artist_name)
        if isinstance(lyrics_data, str):  # Check if there was an error
            error = lyrics_data
            lyrics_data = None
    return render_template('index.html', lyrics_data=lyrics_data, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1990, debug=True)
