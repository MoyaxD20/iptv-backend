import os
import requests
from flask import Flask, redirect, request, Response

app = Flask(__name__)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = "-1003174009090"  # El ID de tu canal CHAT GPT PRO CUENTAS

@app.route('/stream')
def stream_video():
    message_id = request.args.get('message_id')
    if not message_id:
        return "Falta el parámetro message_id", 400
    
    # 1. Obtener la información del mensaje desde Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChannelMessage?chat_id={CHAT_ID}&message_id={message_id}"
    response = requests.get(url).json()
    
    if not response.get("ok"):
        return "No pude encontrar ese mensaje en el canal", 404

    # 2. Extraer el file_id del video o documento
    msg = response["result"]
    file_id = None
    if "video" in msg:
        file_id = msg["video"]["file_id"]
    elif "document" in msg:
        file_id = msg["document"]["file_id"]
        
    if not file_id:
        return "El mensaje no contiene un video válido", 404

    # 3. Obtener el enlace de descarga real
    file_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
    file_info = requests.get(file_url).json()
    file_path = file_info["result"]["file_path"]
    
    # 4. Construir la URL final de descarga
    download_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    
    # 5. Redirigir al reproductor directamente al archivo de Telegram
    return redirect(download_url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
