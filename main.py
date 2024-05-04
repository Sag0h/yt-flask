import os
from flask import Flask, request, send_file, render_template, after_this_request
from functions import video_downloader, search, song_downloader, playlist_downloader

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form['option']
        filetype = request.form['file_type']

        if option == 'url':
            playlist = request.form['is_playlist']
            url = request.form['url']
            if playlist == 'no':
                if filetype == 'song':
                    song_path = song_downloader(url)
                    if song_path == "error":
                        return render_template('index.html', file_path="error")
                    return render_template('index.html', file_path=song_path)
                else:
                    video_path = video_downloader(url)
                    if video_path == "error":
                        return render_template('index.html', file_path="error")
                    return render_template('index.html', file_path=video_path)
            elif playlist == 'yes':
                file_path = playlist_downloader('song', url)
                if file_path == "error":
                    return render_template('index.html', file_path="error")
                return render_template('index.html', file_path=file_path)
        elif option == 'search':
            query = request.form['search_query']
            results = search(query)
            return render_template('search.html', results=results)
    elif (request.method == 'GET') and ('file_path' in request.args):
        file_path = request.args['file_path']
        print(file_path)
        return send_file(file_path, as_attachment=True)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
