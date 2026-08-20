import os
import re
from quart import Quart, request, Response
from telethon import TelegramClient

app = Quart(__name__)

# Leemos las llaves de entorno que acabas de configurar en Render
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# Inicializamos el cliente de Telegram
client = TelegramClient('bot_session', API_ID, API_HASH)

@app.before_serving
async def startup():
    # Arrancamos la sesión del bot al prender el servidor
    await client.start(bot_token=BOT_TOKEN)

@app.route('/stream/<int:chat_id>/<int:message_id>.mp4')
async def stream_video(chat_id, message_id):
    # Verificamos conexión
    if not client.is_connected():
        await client.connect()

    # Buscamos el mensaje exacto que contiene tu película/serie
    message = await client.get_messages(chat_id, ids=message_id)
    if not message or not message.media:
        return "Video no encontrado", 404

    file_size = message.document.size

    # 🔥 MAGIA PARA EXOPLAYER: Manejo de fragmentos (Range Requests)
    range_header = request.headers.get('Range')
    offset = 0
    limit = file_size - 1

    if range_header:
        match = re.search(r'bytes=(\d+)-(\d*)', range_header)
        if match:
            offset = int(match.group(1))
            if match.group(2):
                limit = int(match.group(2))

    length = limit - offset + 1
    chunk_size = 1024 * 1024  # Descargamos en bloques de 1MB a máxima velocidad

    # Función generadora que envía el video como si fuera un grifo de agua
    async def generate():
        async for chunk in client.iter_download(message.media, offset=offset, request_size=chunk_size):
            yield chunk

    # Cabeceras que engañan a ExoPlayer para que crea que es un servidor VOD normal
    headers = {
        'Content-Type': 'video/mp4',
        'Accept-Ranges': 'bytes',
        'Content-Length': str(length),
        'Content-Range': f'bytes {offset}-{limit}/{file_size}',
    }

    status_code = 206 if range_header else 200
    return Response(generate(), status=status_code, headers=headers)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
