import requests
import json
import os
from dotenv  import load_dotenv

load_dotenv(dotenv_path="./.env")


API_KEY = os.getenv("API_KEY")
CHANNEL_HANDEL = 'MrBeast'
max_results = 50

def get_playlsitID():

    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDEL}&key={API_KEY}'

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        channel_items = data["items"][0]
        channel_playlistId = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(channel_playlistId)
        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise e
    

    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistId}&key=[YOUR_API_KEY]'
    playlistId = get_playlsitID()

def get_videoID(playlistId):
    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistId}&key=[YOUR_API_KEY]'
    video_id = []
    pageToken = None

    try:

        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

    except requests.exceptions.RequestException as e:
        raise e


if __name__ == "__main__":
    print("get_playlistID will be exceuted")
    playlistId =get_playlsitID()
