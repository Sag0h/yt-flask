import pytube
from moviepy.audio.io.AudioFileClip import AudioFileClip

import os
from datetime import datetime, timedelta
import zipfile

download_path = "downloads/"


def clean_downloads():
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
            'author': result.author
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

    video_title = video.title

    if not os.path.exists(download_path):
        os.makedirs(download_path)

    found_video = video.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
    print(f"Downloading {video_title} from Youtube")
    found_video.download(output_path=download_path)
    video_path = download_path + video_title + ".mp4"
    print("Done.")
    return f"{video_path}"

def song_downloader(url):
    clean_downloads() # Limpiar descargas antiguas para ahorrar espacio en disco. luego de 5 horas de descargado
    
    try:
        song = pytube.YouTube(url)
    except pytube.exceptions.VideoUnavailable:
        print("no se encontro el video de youtube")
        return "error"

    name = song.streams.get_audio_only().default_filename
    namemp3 = name.replace(".mp4", ".mp3")
    print(f"Downloading {song.title} from Youtube")
    song.streams.get_audio_only().download(output_path=download_path)
    print("Done.")
    convert_mp4_to_mp3(download_path+name, download_path+namemp3)
    return download_path+namemp3



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

