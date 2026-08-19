import os
import requests
from flask import Flask, Response, redirect, request

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

@app.route('/stream')
def stream_video():
    # El usuario enviará el ID del mensaje, por ejemplo: /stream?chat_id=-1002914692761&message_id=6
    chat_id = request.args.get('chat_id')
    message_id = request.args.get('message_id')
    
    # URL de la API de Telegram para obtener la información del archivo
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id=..." 
    
    # Nota: Para archivos privados, lo mejor es redirigir al bot
    # Por ahora, probaremos la redirección simple
    return f"Conectando al grupo {chat_id} mensaje {message_id}..."

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
