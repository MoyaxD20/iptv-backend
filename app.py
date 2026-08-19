import os
import requests
from flask import Flask, redirect, request

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "-1003174009090"  # Tu canal CHAT GPT PRO CUENTAS

@app.route('/')
def home():
    return "¡El servidor de streaming de la Apoderada está activo y funcionando!", 200

@app.route('/stream')
def stream_video():
    message_id = request.args.get('message_id')
    if not message_id:
        return "Falta el parámetro message_id", 400
    
    # Telegram permite obtener mensajes de un canal reenviándolos o consultando.
    # Pero el método más estable para un Bot en un canal es usar getUpdates reciente
    # o utilizar el enlace directo de exportación si el archivo es accesible.
    
    # Truco directo: Como tu bot es administrador del canal, 
    # podemos usar la API para buscar el file_id mediante un forward temporal o consulta.
    # Alternativa limpia: Si el bot usa el método de exportación de chat:
    
    # Vamos a pedir la información usando un endpoint compatible de la API de Telegram:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/forwardMessage"
    payload = {
        "chat_id": CHAT_ID,
        "from_chat_id": CHAT_ID,
        "message_id": int(message_id),
        "disable_notification": True
    }
    
    # Al reenviar el mensaje al propio chat (o a una variable), la API nos devuelve 
    # el objeto completo del mensaje con su 'video' o 'document' y su 'file_id'.
    res = requests.post(url, json=payload).json()
    
    if not res.get("ok"):
        return f"Error al obtener el contenido de Telegram: {res.get('description', 'Desconocido')}", 400
        
    msg = res["result"]
    file_id = None
    if "video" in msg:
        file_id = msg["video"]["file_id"]
    elif "document" in msg:
        file_id = msg["document"]["file_id"]
    elif "audio" in msg:
        file_id = msg["audio"]["file_id"]
        
    if not file_id:
        return "El mensaje no contiene un archivo multimedia válido", 400
        
    # Obtenemos la ruta real de descarga en los servidores de Telegram
    file_info_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    file_info = requests.get(file_info_url).json()
    
    if not file_info.get("ok"):
        return "No se pudo obtener la ruta del archivo", 500
        
    file_path = file_info["result"]["file_path"]
    download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    
    # Redirigimos al ExoPlayer directamente al flujo del video
    return redirect(download_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
