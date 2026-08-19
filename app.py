import os
from flask import Flask, redirect, request

app = Flask(__name__)

# Diccionario temporal con un video de prueba público, seguro y rápido
VIDEOS_PRUEBA = {
    "test": "https://www.w3schools.com/html/mov_bbb.mp4"
}

@app.route('/')
def home():
    return "¡El servidor de streaming de la Apoderada está activo y en modo de prueba!", 200

@app.route('/stream')
def stream_video():
    message_id = request.args.get('message_id')
    
    if not message_id:
        return "Falta el parámetro message_id", 400
    
    # Buscamos el video en nuestra lista de prueba
    video_url = VIDEOS_PRUEBA.get(str(message_id))
    
    if not video_url:
        return "Video no encontrado en la lista de prueba", 404
        
    # Redirección limpia e inmediata al archivo MP4
    return redirect(video_url)

if __name__ == '__main__':
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
