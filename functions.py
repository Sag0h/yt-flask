import pytube
from moviepy.audio.io.AudioFileClip import AudioFileClip

import os
from datetime import datetime, timedelta
import zipfile
import re

download_path = "downloads/"

# Función para limpiar nombres de archivo
def clean_filename(filename):
    # Remover caracteres especiales
    cleaned_filename = re.sub(r'[^a-zA-Z0-9\.\-\\/ ]', '', filename)
    return cleaned_filename

def clean_videoname(filename):
    # Verificar si hay un punto en el nombre del archivo
    if '.' in filename:
        # Dividir el nombre del archivo en nombre y extensión
        name, extension = filename.rsplit('.', 1)
        # Remover caracteres especiales del nombre del archivo
        cleaned_name = re.sub(r'[^\w\s.-]', '', name)
        # Reemplazar múltiples espacios con uno solo
        cleaned_name = re.sub(r'\s+', ' ', cleaned_name)
        # Volver a unir el nombre del archivo con su extensión
        cleaned_filename = cleaned_name.strip() + '.' + extension
    else:
        # Si no hay punto, solo remover caracteres especiales
        cleaned_filename = re.sub(r'[^\w\s.-]', '', filename)
        # Reemplazar múltiples espacios con uno solo
        cleaned_filename = re.sub(r'\s+', ' ', cleaned_filename)
        cleaned_filename = cleaned_filename.strip()
    cleaned_filename = remove_emojis(cleaned_filename)
    return cleaned_filename

def contains_emojis(text):
    # Utiliza una expresión regular para buscar emojis en el texto
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    # Devuelve True si encuentra emojis, False de lo contrario
    return bool(emoji_pattern.search(text))

def remove_emojis(text):
    # Verifica si hay emojis en el texto
    if contains_emojis(text):
        # Utiliza una expresión regular para eliminar los emojis
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        # Elimina los emojis del texto
        return emoji_pattern.sub(r'', text)
    else:
        # Si no hay emojis, devuelve el texto sin cambios
        return text


def clean_downloads():
    
    if os.path.exists(download_path):
        for file in os.listdir(download_path):
            file_path = os.path.join(download_path, file)
            mod_time = os.path.getmtime(file_path)
            mod_datetime = datetime.fromtimestamp(mod_time)
            time_difference = datetime.now() - mod_datetime
            if time_difference > timedelta(hours=5):
                os.remove(file_path)


def search(query):
    search = pytube.Search(query)
    list_of_results = search.results
    results_list = []
    for result in list_of_results:
        result_dict = {
            'title': result.title,
            'thumbnail_url': result.thumbnail_url,
            'duration': result.length,
            'author': result.author,
            'url': result.watch_url,
        }
        results_list.append(result_dict)
    return results_list


def convert_mp4_to_mp3(mp4, mp3):
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3.replace(".mp4", "")) 
    mp4_without_frames.close()
    os.remove(mp4)

def video_downloader(url):
    """
    Descarga un video de YouTube.

    Args:
    - url (str): URL del video.
    """
    clean_downloads() # Limpiar descargas antiguas para ahorrar espacio en disco. luego de 5 horas de descargado

    try:
        video = pytube.YouTube(url)
    except pytube.exceptions.VideoUnavailable:
        print("no se encontro el video de youtube")
        return "error"

    video_title = clean_videoname(video.title)

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    found_video = video.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
    print(f"Downloading {video_title} from Youtube")
    found_video.download(filename=video_title+".mp4", output_path=download_path)
    video_path = download_path +video_title + ".mp4"
    video_name = clean_filename(video_path)
    print("Done.")
    return f"{video_name}"

def song_downloader(url):
    clean_downloads() # Limpiar descargas antiguas para ahorrar espacio en disco. luego de 5 horas de descargado
    
    try:
        song = pytube.YouTube(url)
    except pytube.exceptions.VideoUnavailable:
        print("no se encontro el video de youtube")
        return "error"

    name = song.streams.get_audio_only().default_filename
    namemp3 = clean_videoname(name.replace(".mp4", ".mp3"))
    print(f"Downloading {song.title} from Youtube")
    song.streams.get_audio_only().download(output_path=download_path)
    print("Done.")
    song_path = download_path + namemp3
    song_name = clean_filename(song_path)
    convert_mp4_to_mp3(clean_filename(download_path+name), song_name)
    return song_name

def playlist_downloader(filetype, url):
    playlist_path = download_path + "playlist/"

    try:
        p = pytube.Playlist(url)
    except pytube.exceptions.VideoUnavailable:
        print("No se encontro la playlist")
        return "error"

    i = 1
    for v in p.videos:
        if filetype == 'song':
            name = v.streams.get_audio_only().default_filename
            namemp3 = name.replace(".mp4", ".mp3")
            print(f'({i}/{p.length}) - Downloading from: {p.title} - {v.title}')
            v.streams.get_audio_only().download(output_path=playlist_path)
            print(f"({i}/{p.length}) - Done.")
            convert_mp4_to_mp3(playlist_path + name, playlist_path + namemp3)
        else:
            print(f'({i}/{p.length}) - Downloading from: {p.title} - {v.title}')
            v.streams.get_highest_resolution().download(output_path=playlist_path)
            print(f"({i}/{p.length}) - Done.")
        i = i + 1
    zip_folder(playlist_path, "playlist" + '.zip')
    return "playlist.zip"     

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

