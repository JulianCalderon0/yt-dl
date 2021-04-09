import requests
from pytube import YouTube
import json


def search(q, key):
    url = "https://www.googleapis.com/youtube/v3/search"
    parameters = {
        "q": q,
        "part": "id,snippet",
        "type": "video",
        "maxResults": 8,
        "key": key,
    }

    # Retrieve data
    response = requests.get(url, params=parameters)
    if response.status_code in (400, 403):
        return "error"
    data = response.json()

    # Reformat data
    data = data["items"]
    clean_data = {}
    for item in data:
        values = {
            "id": item["id"]["videoId"],
            "channel": item["snippet"]["channelTitle"],
            "description": item["snippet"]["description"],
            "date": item["snippet"]["publishedAt"],
            "thumbnail": item["snippet"]["thumbnails"]["high"],
        }
        clean_data[item["snippet"]["title"]] = values
    clean_data

    return clean_data


def download(id, download_folder):
    # Download video
    url = "https://www.youtube.com/watch?v=" + id
    yt = YouTube(url)
    yt.streams.first().download(download_folder)


def download_mp3(id, download_folder):
    url = "https://www.youtube.com/watch?v=" + id
    yt = YouTube(url)
    yt.streams.filter(only_audio=True).first().download(download_folder)


def get_path(path):
    return path


def create_settings():
    # Create empty settings.json
    with open(get_path("resources/settings.json"), "w") as f:
        data = {"key": "", "folder": ""}
        json.dump(data, f)
