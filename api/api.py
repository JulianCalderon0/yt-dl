import requests
from pytube import YouTube

EXITO = 200
ERROR = -1
MAX_RESULTADOS = 8
URL_API = "https://www.googleapis.com/youtube/v3/search"


def buscar(consulta, clave):
    url = URL_API
    parametros = {
        "q": consulta,
        "part": "id,snippet",
        "type": "video",
        "maxResults": MAX_RESULTADOS,
        "key": clave,
    }

    respuesta = requests.get(url, params=parametros)

    if respuesta.status_code != EXITO:
        return ERROR

    data = respuesta.json()

    data = data["items"]
    f_data = {}
    for video in data:
        f_video = {
            "id": video["id"]["videoId"],
            "channel": video["snippet"]["channelTitle"],
            "description": video["snippet"]["description"],
            "date": video["snippet"]["publishedAt"],
            "thumbnail": video["snippet"]["thumbnails"]["high"],
        }
        f_data[video["snippet"]["title"]] = f_video

    return f_data


def descargar_video(id, destino):
    url = "https://www.youtube.com/watch?v=" + id
    yt = YouTube(url)
    yt.streams.get_highest_resolution().download(destino)


def descargar_audio(id, destino):
    url = "https://www.youtube.com/watch?v=" + id
    yt = YouTube(url)
    yt.streams.get_audio_only().download(destino)
