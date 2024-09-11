from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time
import random
import urllib.parse

app = Flask(__name__)

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
        
        # Send a GET request to the provided URL with a User-Agent header
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse the content of the response using BeautifulSoup
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        # Find all tables with the class "table table-condensed"
        tables = soup.find_all("table", {"class": "table table-condensed"})

        table_data = set()  # Use a set to store unique song title and URL pairs

        # Iterate over each table found
        for table in tables:
            rows = table.find_all("tr")  # Find all rows in the table
            for row in rows:
                link = row.find("a")  # Find anchor tags within the rows
                if link:
                    song_title = link.text.strip()  # Extract and clean the song title
                    song_url = link.get("href")  # Get the URL from the anchor tag
                    if song_url:
                        # Filter out links that are not related to lyrics
                        if "/lyrics/" in song_url:
                            # Construct the full URL for the song
                            full_url = f"https://www.azlyrics.com{song_url}"
                            # Add the song title and URL as a tuple to the set
                            table_data.add((song_title, full_url))

        # Convert the set of tuples back to a list
        table_data = list(table_data)

        return table_data  # Return the list of song titles and URLs
    except requests.RequestException as e:
        # Print error message if there is an issue with the request
        print(f"Error fetching lyrics: {e}")
        return []  # Return an empty list in case of error

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles GET and POST requests to the root URL.
    Returns:
        str: Rendered HTML template.
    """
    if request.method == 'POST':
        # Get the artist name from the form submission
        artist_name = request.form['artist']
        # Encode the artist name to be safely included in the URL
        encoded_artist_name = urllib.parse.quote_plus(artist_name)
        # Construct the search URL with the encoded artist name
        search_url = f"https://search.azlyrics.com/search.php?q={encoded_artist_name}&x=7a9e51768f99ae8e4928f9b8f04dbb638c8bdad95502d5f706036bb982e19244"
        print(f"Constructed URL: {search_url}")

        # Fetch lyrics data using the constructed search URL
        lyrics_data = fetch_lyrics(search_url)
        
        if not lyrics_data:
            # Render the template with an error message if no data was found or an error occurred
            return render_template('index.html', error="No songs found or an error occurred.")
        
        # Render the template with the fetched lyrics data
        return render_template('index.html', lyrics_data=lyrics_data, artist_name=artist_name)
    
    # Render the template for GET requests
    return render_template('index.html')

if __name__ == '__main__':
    # Run the Flask application on all network interfaces, port 1990, with debugging enabled
    app.run(host='0.0.0.0', port=1990, debug=True)
