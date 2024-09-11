# Lyric-scrapper

Lyric-scrapper is a Flask-based web application that allows you to search for song lyrics by artist name. It scrapes lyrics from AzLyrics.com and displays the results in a user-friendly interface.

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
   git clone https://github.com/metrik420/Lyric-scrapper.git
   cd Lyric-scrapper
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**

   ```bash
   python scrappy.py
   ```

   Open your web browser and go to `http://localhost:1990` to access the application.

## List of Features

- Search for song lyrics by artist name
- Display search results in a table format
- View lyrics in a new tab
- User-friendly interface with responsive design
- Error handling with a sticky banner for error messages
