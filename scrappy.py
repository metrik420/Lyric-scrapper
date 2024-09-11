from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse

app = Flask(__name__)

# Add a list of user agents to randomize from
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
    # Add more User-Agent strings as needed
]

# Helper function to fetch lyrics with proper headers and delays
def fetch_lyrics(url):
    """
    Fetches lyrics from the given URL.
    Args:
        url (str): The URL to fetch data from.
    Returns:
        list: A list of tuples containing song titles and their corresponding URLs.
    """
    try:
        # Randomize delay to mimic human behavior and avoid detection as a bot
        time.sleep(random.uniform(2.0, 5.0))
        
        # Randomly select a user agent
        headers = {"User-Agent": random.choice(USER_AGENTS)}
        
        # Send a GET request to the provided URL with randomized headers
        response = requests.get(url, headers=headers)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse the content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Extract tables with class "table table-condensed"
        tables = soup.find_all("table", {"class": "table table-condensed"})

        table_data = set()

        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                link = row.find("a")
                if link:
                    song_title = link.text.strip()
                    song_url = link.get("href")
                    if song_url and "/lyrics/" in song_url:
                        full_url = f"https://www.azlyrics.com{song_url}" if not song_url.startswith('http') else song_url
                        table_data.add((song_title, full_url))

        return list(table_data)
    
    except requests.RequestException as e:
        print(f"Error fetching lyrics: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles GET and POST requests to the root URL.
    Returns:
        str: Rendered HTML template.
    """
    if request.method == 'POST':
        artist_name = request.form['artist']
        encoded_artist_name = urllib.parse.quote_plus(artist_name)
        search_url = f"https://search.azlyrics.com/search.php?q={encoded_artist_name}&x=7a9e51768f99ae8e4928f9b8f04dbb638c8bdad95502d5f706036bb982e19244"
        
        lyrics_data = fetch_lyrics(search_url)
        
        if not lyrics_data:
            return render_template('index.html', error="No songs found or an error occurred.")
        
        return render_template('index.html', lyrics_data=lyrics_data, artist_name=artist_name)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1990, debug=True)
