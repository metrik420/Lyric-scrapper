# Lyric Scraper Flask App

This Python Flask application allows users to search for song lyrics using a simple web interface.

## Requirements

- Python 3.6+
- Flask
- Requests
- BeautifulSoup4

## Installation

1. Clone the repository or download the zip file.

2. Navigate to the project directory and install dependencies:
   ```bash
   pip install -r requirements.txtRun the Flask application:python scrappy.pyOpen a web browser and go to http://127.0.0.1:1990 to use the app.Python Script (scrappy.py): You already have a working script for Flask. Make sure that the script references the correct path for the HTML template (templates/index.html). Here's the modified scrappy.py script for easy setup:from flask import Flask, request, render_template
import requests
from bs4 import BeautifulSoup
import os
import random
import time

app = Flask(__name__)

def fetch_lyrics(url, artist_name):
    """Fetch song lyrics from the provided URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
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
                        song_lyrics = "..."  # Scrape or mock lyrics if necessary
                        table_data.append([i, artist_name, song_title, song_lyrics, song_url])
        return table_data

    except requests.RequestException as e:
        return f"Error fetching data: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        artist_name = request.form['artist_name'].strip().replace(" ", "+")
        url = f"https://search.azlyrics.com/search.php?q={artist_name}&w=lyrics&p=1"

        # Add a delay to mimic random user activity
        time.sleep(random.uniform(1, 3))

        lyrics_data = fetch_lyrics(url, artist_name)
        return render_template('index.html', lyrics_data=lyrics_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1990, debug=True)HTML File (templates/index.html): Make sure the HTML file is inside a templates folder. Here's an example of index.html:<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <title>Lyric Search</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f2f5;
            margin: 0;
            padding: 0;
            color: #333;
        }
        .container {
            width: 90%;
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
            background: #fff;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
            border-radius: 12px;
        }
        h1 {
            color: #4CAF50;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5rem;
        }
        form {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 30px;
        }
        label, input {
            font-size: 1.2rem;
        }
        input[type="text"] {
            padding: 10px;
            margin-right: 20px;
            width: 300px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            font-size: 1.2rem;
            background-color: #4CAF50;
            color: #fff;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        th, td {
            padding: 16px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: #fff;
            font-size: 1.2rem;
            text-transform: uppercase;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
            transition: background-color 0.3s ease;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Search for Lyrics</h1>
        <form method="post">
            <label for="artist_name">Enter artist name:</label>
            <input type="text" id="artist_name" name="artist_name" required>
            <button type="submit">Search</button>
        </form>

        {% if lyrics_data %}
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Artist</th>
                    <th>Song Title</th>
                    <th>Song Lyrics</th>
                    <th>URL</th>
                </tr>
            </thead>
            <tbody>
                {% for item in lyrics_data %}
                <tr>
                    <td>{{ item[0] }}</td>
                    <td>{{ item[1] }}</td>
                    <td>{{ item[2] }}</td>
                    <td>{{ item[3] }}</td>
                    <td><a href="{{ item[4] }}" target="_blank">Link</a></td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}
    </div>
</body>
</html>6. Installation Instructions:Ensure the user has Python 3 installed.After downloading or cloning the project, the user needs to run:pip install -r requirements.txtThen, they can run the application using:python scrappy.pyThe user can now navigate to http://127.0.0.1:1990 to access the web interface.
