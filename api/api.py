import requests
from pytube import YouTube


EXITO = 200
ERROR = -1
MAX_RESULTADOS = 8


def buscar(consulta, clave):
    """
    Recibe una consulta y una clave de la API de Google. LLama al metodo de busqueda de la API.

    Devuelve un diccionario de MAX_RESULTADOS, donde cada clave es el titulo del video,
    y sus valores son las propiedades del video.

    Devuelve ERROR en caso de ERROR.
    """

    url = "https://www.googleapis.com/youtube/v3/search"
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
    """
    Recibe la ID de un video de youtube y una carpeta de destino.

    Descarga la opcion com mayor resolucion del video en la carpeta especificada.
    """

    url = "https://www.youtube.com/watch?v=" + id
    yt = YouTube(url)
    yt.streams.get_highest_resolution().download(destino)
