import os
import requests
from flask import Flask, redirect, request, Response

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
    
    # Telegram no tiene una función directa 'getChannelMessage', pero podemos usar
    # un truco limpio de la API o redirigir usando la estructura del canal si es público,
    # o consultar la API oficial de Bot para obtener actualizaciones recientes.
    # Una opción robusta para bots en canales es usar getChat o verificar el mensaje mediante forward:
    
    # Intentemos obtener el archivo directamente usando la API de Telegram para mensajes de canal:
    # Nota: Los canales a veces requieren que el bot sea administrador con plenos poderes (ya lo es).
    
    api_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    # Como alternativa rápida y ultra estable para streaming:
    # Vamos a devolver una respuesta clara para validar que el servidor recibe el ID perfecto.
    
    return f"Recibí la petición para el video con ID: {message_id} en el canal {CHAT_ID}. Ajustando enlace de redirección...", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
