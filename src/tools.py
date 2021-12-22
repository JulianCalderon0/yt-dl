import requests
from pytube import YouTube


def search(query, key):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "q": query,
        "part": "id,snippet",
        "type": "video",
        "maxResults": 8,
        "key": key,
    }

    response = requests.get(url, params=params)
    if response.status_code in (400, 403):
        return "error"
    data = response.json()

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
    url = "https://www.youtube.com/watch?v=" + id
    yt = YouTube(url)
    yt.streams.get_highest_resolution().download(download_folder)


def download_audio(id, download_folder):
    url = "https://www.youtube.com/watch?v=" + id
    yt = YouTube(url)
    yt.streams.filter(only_audio=True).first().download(download_folder)


def get_path(path):
    return path
