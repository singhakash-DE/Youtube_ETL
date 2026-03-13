import requests
import json
import os
from dotenv  import load_dotenv
from datetime import date

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

        #print(channel_playlistId)
        return channel_playlistId

    except requests.exceptions.RequestException as e:
        raise e
    


def get_videoID(playlistId):
    base_url = f'https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={max_results}&playlistId={playlistId}&key={API_KEY}'
    video_ids = []
    pageToken = None

    try:

        while True:
            url = base_url
            if pageToken:
                url += f"&pageToken={pageToken}"
            
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            data = response.json()
            #print(data)
            for item in data.get('items',[]):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id)

            pageToken = data.get('nextPageToken')

            if not pageToken:
                break
        return video_ids
    except requests.exceptions.RequestException as e:
        raise e


def extract_videoId_data(video_ids):
    video_url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id=smDPnIdlkhM&key={API_KEY}' 
    extracted_data = []

    def batch_list(video_id_list,batch_size):
        for video_id in range(0,len(video_id_list),batch_size):
            yield video_id_list[video_id: video_id + batch_size]
    try:
        for batch in batch_list(video_ids,max_results):
            video_ids_str = ",".join(batch)
            video_url = f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails&part=snippet&part=statistics&id={video_ids_str}&key={API_KEY}' 
            response = requests.get(video_url)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items',[]):
                video_id = item['id']
                snippet = item['snippet']
                contentDetails = item['contentDetails']
                statistics = item['statistics']
                video_data = {
                    "video_id" : video_id,
                    "title" : snippet['title'],
                    "publishedAt" : snippet['publishedAt'],
                    "duration" : contentDetails['duration'],
                    "viewCount" : statistics.get('viewCount',None),
                    "likeCount" : statistics.get('likeCount',None),
                    "commentCount": statistics.get('commentCount',None)
                }

                extracted_data.append(video_data)
    
        return extracted_data

    except requests.exceptions.RequestException as e:
        raise e

def  save_to_json(extract_videoId_data):
    file_path = f"./data/YT_data_{date.today()}.json"

    with open(file_path,"w",encoding="utf-8") as json_outfiles:
        json.dump(extract_videoId_data,json_outfiles,indent=4,ensure_ascii=False)



if __name__ == "__main__":
    print("get_playlistID will be exceuted")
    playlistId =get_playlsitID()
    video_ids=get_videoID(playlistId)
    video_data = extract_videoId_data(video_ids)
    save_to_json(video_data)

