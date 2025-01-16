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
import json
from bs4 import BeautifulSoup
from tabulate import tabulate
import urllib.parse
import inquirer
import re
from tqdm import tqdm   
import time

SONGSTERR_URL = "https://www.songsterr.com"

def convert_tuning(midi_arr):
    midi_to_note = {
        0: "C", 1: "C#", 2: "D", 3: "D#", 4: "E", 5: "F", 6: "F#",
        7: "G", 8: "G#", 9: "A", 10: "A#", 11: "B",
        12: "C", 13: "C#", 14: "D", 15: "D#", 16: "E", 17: "F", 18: "F#",
        19: "G", 20: "G#", 21: "A", 22: "A#", 23: "B",
        24: "C", 25: "C#", 26: "D", 27: "D#", 28: "E", 29: "F", 30: "F#",
        31: "G", 32: "G#", 33: "A", 34: "A#", 35: "B",
        36: "C", 37: "C#", 38: "D", 39: "D#", 40: "E", 41: "F", 42: "F#",
        43: "G", 44: "G#", 45: "A", 46: "A#", 47: "B",
        48: "C", 49: "C#", 50: "D", 51: "D#", 52: "E", 53: "F", 54: "F#",
        55: "G", 56: "G#", 57: "A", 58: "A#", 59: "B",
        60: "C", 61: "C#", 62: "D", 63: "D#", 64: "E", 65: "F", 66: "F#",
        67: "G", 68: "G#", 69: "A", 70: "A#", 71: "B",
        72: "C", 73: "C#", 74: "D", 75: "D#", 76: "E", 77: "F", 78: "F#",
        79: "G", 80: "G#", 81: "A", 82: "A#", 83: "B",
        84: "C", 85: "C#", 86: "D", 87: "D#", 88: "E", 89: "F", 90: "F#",
        91: "G", 92: "G#", 93: "A", 94: "A#", 95: "B",
        96: "C", 97: "C#", 98: "D", 99: "D#", 100: "E", 101: "F", 102: "F#",
        103: "G", 104: "G#", 105: "A", 106: "A#", 107: "B",
        108: "C", 109: "C#", 110: "D", 111: "D#", 112: "E", 113: "F", 114: "F#",
        115: "G", 116: "G#", 117: "A", 118: "A#", 119: "B",
        120: "C", 121: "C#", 122: "D", 123: "D#", 124: "E", 125: "F", 126: "F#",
        127: "G"
    }
    
    # Convert MIDI numbers to note names
    note_names = [midi_to_note[note] for note in midi_arr if note in midi_to_note][::-1]
    
    return ' '.join(note_names)

def process_id(song_id):
    api_url = SONGSTERR_URL + f"/api/meta/{song_id}"
    # print("API url:", api_url)
    response = requests.get(api_url)
    response_json = json.loads(response.text)
    try:
        tuning = response_json['tracks'][0]['tuning']
        tuning = convert_tuning(tuning)
    except: 
        tuning = "NA"
    return tuning

def process_link(link):
    # link = "https://www.songsterr.com/a/wsa/necrophagist-stabwound-tab-s48300"

    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Find the script tag with id="state"
    script_tag = soup.find('script', id='state')
    script_content = script_tag.string
    data = json.loads(script_content)
    song_id = data['route']['params']['songId']
    artist = data['meta']['current']['artist']
    song_name = data['meta']['current']['title']
    print("Artist:", artist)
    print("Song Name:", song_name)
    print("Song ID:", song_id)
    api_url = SONGSTERR_URL + f"/api/meta/{song_id}"
    print("API url:", api_url)
    response = requests.get(api_url)
    response_json = json.loads(response.text)
    tuning = response_json['tracks'][0]['tuning']
    print("Tuning:", convert_tuning(tuning))

    # # response = requests.get(f'https://www.songsterr.com/api/meta/{song_id}/revisions')
    # response_json = json.loads(response.text)
    # latest_revision = response_json[0]
    # revision_source = latest_revision['source']

    # save_filename = artist + " - " + song_name + ".gp"
    # print(save_filename)

    # try:
    #     # Send a GET request to the URL
    #     response = requests.get(revision_source, stream=True)
    #     response.raise_for_status()  # Raise an error if the request failed

    #     # Write the response content to a file in binary mode
    #     # with open(save_filename, 'wb') as file:
    #     #     for chunk in response.iter_content(chunk_size=8192):  # Use chunks to handle large files
    #     #         file.write(chunk)

    #     print(f"File downloaded successfully as {save_filename}")

    # except requests.exceptions.RequestException as e:
    #     print(f"Failed to download the file: {e}")

def process_pattern(pattern, top_n=5):
    encoded_pattern = urllib.parse.quote(pattern)
    # url = f"https://www.songsterr.com/?pattern={encoded_pattern}"
    url = f"{SONGSTERR_URL}/?pattern={encoded_pattern}"
    print(url)
    r = requests.get(url)
    # time.sleep(3)
    soup = BeautifulSoup(r.content, 'html.parser')

    songs_div = soup.find('div', {'data-list': 'songs'})
    songs_list = []
    try:
        songs = songs_div.find_all('a', {'class': 'B0cew'})
        songs = songs[:top_n]
        for i, song in enumerate(tqdm(songs, desc="Processing songs", unit="song")):
            # if i >= 10:
            #     break
            song_name = song.find('div', {'data-field': 'name'}).text
            artist_name = song.find('div', {'data-field': 'artist'}).text
            difficulty = song.find('span')['title']
            song_link = f"{SONGSTERR_URL}{song['href']}"
            song_id = re.search(r's(\d+)', song['href']).group(1)

            api_url = SONGSTERR_URL + f"/api/meta/{song_id}"
            tuning = process_id(song_id)

            songs_list.append([song_name, artist_name, tuning])
            # print(f"Song Name: {song_name}, Artist: {artist_name}, Title: {span_title}, Href: {song_href}")
    except Exception as e:
        print(e)
        print("No songs found")

    # print(tabulate(songs_list, headers=["Song Name", "Artist", "Title", "Href"]))

    # Format choices for inquirer
    choices = [
        f"{song[0]:<30} | {song[1]:<20} | {song[2]}"
        for song in songs_list
    ]

    # Use inquirer to select songs
    questions = [
        inquirer.Checkbox('songs',
                          message="Select songs to download ([SPACE] to select)",
                          choices=choices,
                          ),
    ]
    answers = inquirer.prompt(questions)
    selected_songs = [song for song in songs_list if f"{song[0]} by {song[1]}" in answers['songs']]
    print("Selected songs:", selected_songs)

def main():
    parser = argparse.ArgumentParser(description="Choose method of Songsterr downloading")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('-l', '--link', help="Link mode")
    group.add_argument('-p', '--pattern', help="Pattern mode")
    parser.add_argument('-n', '--number', type=int, default=5, help="Number of top results to display in pattern mode")


    args = parser.parse_args()

    if args.link:
        process_link(args.link)
    elif args.pattern:
        process_pattern(args.pattern, args.number)

if __name__ == '__main__':
    main()