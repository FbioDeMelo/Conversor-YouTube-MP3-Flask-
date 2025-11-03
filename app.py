from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    if not url:
        return "Por favor, insira uma URL válida."

    try:
        # Cria um diretório temporário
        temp_dir = tempfile.mkdtemp()
        output_path = os.path.join(temp_dir, "%(title)s.%(ext)s")

        # Configurações do yt_dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        return send_file(filename, as_attachment=True)

    except Exception as e:
        return f"Erro ao baixar: {e}"

if __name__ == '__main__':
    app.run(debug=True)
