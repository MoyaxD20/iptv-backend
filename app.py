import os
from flask import Flask, redirect, request

app = Flask(__name__)

# Diccionario temporal con un video de prueba en formato MP4 puro
VIDEOS_PRUEBA = {
    "test": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
}

@app.route('/')
def home():
    return "¡Servidor de prueba activo para la app de Android TV!", 200

@app.route('/stream')
def stream_video():
    message_id = request.args.get('message_id')
    if not message_id:
        return "Falta el parámetro message_id", 400
    
    # Buscamos el video en nuestra lista de prueba
    video_url = VIDEOS_PRUEBA.get(str(message_id))
    
    if not video_url:
        return "Video no encontrado", 404
        
    # Redirección limpia al archivo MP4
    return redirect(video_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
