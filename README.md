# Scrappy Lyrics Search

Scrappy Lyrics Search is a Flask-based web application that allows you to search for song lyrics by artist name. It scrapes lyrics from AzLyrics.com and displays the results in a user-friendly interface.

## Requirements

- Python 3.x
- Flask
- Requests
- BeautifulSoup4

## File Structure

```
Lyric-scrapper/
│
├── scrappy.py            # Flask application script
├── requirements.txt      # List of dependencies
└── templates/
    └── index.html        # HTML template for the web application
```

## Installation

First, ensure you have Python 3.x installed. Open your terminal or command prompt and navigate to the directory where you want to set up the project

1. **Clone the Repository**

   ```bash
   mkdir Lyric-scrapper
   cd Lyric-scrapper
   git clone https://github.com/metrik420/Lyric-scrapper.git
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**

   ```bash
   python3 scrappy.py
   ```

   Open your web browser and go to `http://localhost:1990` to access the application.

## List of Features

1. Flask Application Setup
   - The app is built using Flask and runs on 0.0.0.0:1990 with debugging enabled. It can be accessed by devices on the same network.
2. User-Agent Randomization
   - To avoid detection as a bot, the application uses a list of randomized User-Agent strings, ensuring each request simulates traffic from different browsers.
3. Human-like Request Delays
   - The fetch_lyrics function introduces a random delay (2 to 5 seconds) between requests, mimicking human browsing behavior and reducing the chances of being blocked by the website.
4. Dynamic Search URL Generation
   - Upon form submission, the artist's name is encoded and incorporated into the AzLyrics search URL, dynamically generating the search query for lyrics retrieval.
5. Lyrics Fetching
   - The app sends a GET request to AzLyrics, using BeautifulSoup to parse the HTML and extract song titles and corresponding URLs for lyrics.
6. Robust Error Handling
   -Handles potential HTTP errors or request exceptions. If an error occurs, it logs the issue and ensures the application continues running smoothly without crashing.
7. HTML Parsing for Song Data
   - The app extracts song titles and their corresponding URLs from tables with the class "table table-condensed", specifically targeting links containing /lyrics/.
8. Form Submission Handling
   - The application supports both GET and POST requests:
   - POST: When a user submits an artist name, it retrieves and displays the lyrics.
   - GET: Renders the default search form for user input.
9. Dynamic Template Rendering
    - The index.html template is dynamically updated based on user input. It displays search results (song titles and lyrics) or appropriate error messages if the search fails.
10. Clean URL Construction
    - For each song title, the app ensures the URL is fully constructed, appending the domain (https://www.azlyrics.com) when necessary, ensuring all links work correctly.
11. Search Error Messaging
    - If no songs are found or an error occurs during the fetch process, a user-friendly error message is displayed, helping guide the user on potential issues.
      
This Flask application allows users to search for song lyrics by artist, dynamically generates the search results, and employs multiple techniques to avoid detection by anti-scraping mechanisms.
