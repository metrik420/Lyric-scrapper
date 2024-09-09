import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

def fetch_lyrics(url):
    try:
        # Send request and get content
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        content = response.content

        # Parse HTML content
        soup = BeautifulSoup(content, "html.parser")

        # Find all tables with class "table table-condensed"
        tables = soup.find_all("table", {"class": "table table-condensed"})

        # Prepare data for tabulate
        table_data = []

        for i, table in enumerate(tables, start=1):
            rows = table.find_all("tr")
            for row in rows:
                link = row.find("a")
                if link:
                    song_title = link.text.strip()
                    song_url = link.get("href")
                    if song_url:
                        full_url = f"https://www.azlyrics.com{song_url}"
                        table_data.append([i, song_title, full_url])

        return table_data
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def main():
    # Prompt user for artist name
    artist = input("Enter artist name: ").strip().replace(" ", "+")
    url = f"https://search.azlyrics.com/search.php?q={artist}&w=lyrics&p=1&x=7212ca797bf201758b9641f763c67f2c88a4bc8f3ce6c933097b8401e6ca9453"

    # Fetch lyrics data
    lyrics_data = fetch_lyrics(url)

    # Print the table using tabulate
    headers = ["Table No.", "Song Title", "URL"]
    if lyrics_data:
        print("\nLyric Results:")
        print(tabulate(lyrics_data, headers=headers, tablefmt="grid"))
    else:
        print("No lyrics found or there was an error.")

if __name__ == "__main__":
    main()
