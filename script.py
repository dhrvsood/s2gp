r"""
Song Link: https://www.songsterr.com/a/wsa/necrophagist-stabwound-tab-s48300
Revision Link: https://www.songsterr.com/a/wsa/necrophagist-stabwound-tab-s48300/r981463...r1066276
Download Link: https://gp.songsterr.com/export.663869018.gp

https://www.songsterr.com/api/meta/48300/revisions

response = requests.get(f'https://www.songsterr.com/api/meta/{song_id}/revisions')

Create environment: python -m venv <name>
Activate environment: .\s2gp\Scripts\activate
pip install libraries (requests, beautifulsoup4, tabulate, inquirer)
pip freqeze > requirements.txt
"""
import argparse
import requests
from bs4 import BeautifulSoup
import urllib.parse
import inquirer
from tqdm import tqdm   
from track import Track
import os
from dotenv import load_dotenv

load_dotenv()

SONGSTERR_URL = "https://www.songsterr.com"
MAX_TITLE_LENGTH = 30
MAX_ARTIST_LENGTH = 20
SAVE_DIR = os.getenv('SAVE_DIR')
print(SAVE_DIR)

def truncate_string(s, max_length):
    return s if len(s) <= max_length else s[:max_length-3] + '...'

def download_file(track: Track):
    """
    save directory as environment variable
    folder name - track.artist, create if not created
    file name - track.title + .gp
    source - track.source
    """
    # Create the directory if it doesn't exist
    artist_dir = os.path.join(SAVE_DIR, track.artist)
    os.makedirs(artist_dir, exist_ok=True)

    # Define the save filename
    save_filename = os.path.join(artist_dir, f"{track.title}.gp")

    try:
        # Send a GET request to the URL
        response = requests.get(track.source, stream=True)
        response.raise_for_status()  # Raise an error if the request failed

        # Write the response content to a file in binary mode
        with open(save_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):  # Use chunks to handle large files
                file.write(chunk)

        print(f"File downloaded successfully as {save_filename}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download the file: {e}")

def process_links(links):
    for link in links:
        track = Track(link)
        download_file(track)

def process_pattern(pattern, top_n=5):
    encoded_pattern = urllib.parse.quote(pattern)
    url = f"{SONGSTERR_URL}/?pattern={encoded_pattern}"
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    songs_div = soup.find('div', {'data-list': 'songs'})
    tracks_list = []
    try:
        songs = songs_div.find_all('a', {'class': 'B0cew'})
        songs = songs[:top_n]
        for song in tqdm(songs, desc="Processing songs", unit="song"):  
            href = song['href']
            track = Track(href)
            tracks_list.append(track)
    except Exception as e:
        print(e)
        print("No songs found")

    choices = [
        f"{truncate_string(track.title, MAX_TITLE_LENGTH):<30} | {truncate_string(track.artist, MAX_ARTIST_LENGTH):<20} | {track.tuning}"
        for track in tracks_list
    ]

    # Use inquirer to select songs
    questions = [
        inquirer.Checkbox('songs',
                          message="Select songs to download ([SPACE] to select)",
                          choices=choices,
                          ),
    ]
    answers = inquirer.prompt(questions)
    print(answers)
    selected_songs = [tracks_list[i] for i, choice in enumerate(choices) if choice in answers['songs']]

    # selected_songs = [song for song in songs_list if f"{song[0]} by {song[1]}" in answers['songs']]
    print("Selected songs:", selected_songs)
    for track in selected_songs:
        download_file(track)

def main():
    parser = argparse.ArgumentParser(description="Choose method of Songsterr downloading")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-l', '--links', nargs='+', help="Links mode")
    group.add_argument('-p', '--pattern', help="Pattern mode")
    parser.add_argument('-n', '--number', type=int, default=5, help="Number of top results to display in pattern mode")

    args = parser.parse_args()

    if args.links:
        process_links(args.links)
    elif args.pattern:
        process_pattern(args.pattern, args.number)

if __name__ == '__main__':
    main()