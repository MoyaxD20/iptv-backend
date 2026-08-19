import os
from flask import Flask, redirect, request

app = Flask(__name__)

# Diccionario con tus videos: el número de mensaje apunta a su enlace directo de Telegram
VIDEOS = {
    "2": "https://t.me/c/3174009090/2",  # Puedes poner aquí el enlace directo o el file_id
    # Agrega aquí tus otros videos cuando gustes:
    # "3": "URL_O_ENLACE_3",
}

@app.route('/')
def home():
    return "¡El servidor de streaming de la Apoderada está activo y funcionando!", 200

@app.route('/stream')
def stream_video():
    message_id = request.args.get('message_id')
    if not message_id:
        return "Falta el parámetro message_id", 400
    
    # Busca el video en nuestra lista
    video_url = VIDEOS.get(str(message_id))
    
    if not video_url:
        return "Video no encontrado en la lista", 404
        
    # Redirige de inmediato al reproductor
    return redirect(video_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
