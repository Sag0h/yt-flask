import os
from flask import Flask, request, send_file, render_template, after_this_request
from functions import video_downloader, search, song_downloader, playlist_downloader

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        option = request.form['option']
        filetype = request.form['file_type']
        template = 'index.html'

        print(template)
        if option == 'url':
            url = request.form['url']
            if filetype == 'song':
                song_path = song_downloader(url=url)
                if song_path == "error":
                    return render_template(template, file_path="error")
                return render_template(template, file_path=song_path)
            else:
                video_path = video_downloader(url=url)
                if video_path == "error":
                    return render_template(template, file_path="error")
                return render_template(template, file_path=video_path)
        elif option == 'search':
            query = request.form['search_query']
            results = search(query)
            return render_template('index.html', results=results)
    elif (request.method == 'GET') and ('file_path' in request.args):
        file_path = request.args['file_path']
        file_path = file_path.replace('/', '\\')  # Reemplazar barras diagonales
        file_path = os.path.join(os.getcwd(), file_path)  # Construir la ruta completa
        print(file_path)
        return send_file(file_path, as_attachment=True)
    else:

        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
