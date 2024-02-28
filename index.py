from flask import Flask, render_template, request, redirect, url_for
import yt_dlp

app = Flask(__name__)

def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'static/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict['title']
        file_name = title + '.mp3'
        return file_name

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        file_name = download_audio(url)
        return redirect(url_for('downloaded', file_name=file_name))
    return render_template('index.html')

@app.route('/downloaded/<file_name>')
def downloaded(file_name):
    return render_template('downloaded.html', file_name=file_name)

if __name__ == '__main__':
    app.run(debug=True)
