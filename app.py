import os
from flask import Flask, Response, request

app = Flask(__name__)

@app.route('/')
def home():
    return "¡El servidor de streaming de la Apoderada está activo y funcionando!", 200

@app.route('/stream')
def stream_video():
    # Aquí es donde más adelante conectaremos el puente hacia tu video
    video_url = request.args.get('url')
    if not video_url:
        return "Falta la URL del video", 400
    
    # Render o el servidor redirige el flujo de forma estable a la app
    return f"Reproduciendo contenido desde: {video_url}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)