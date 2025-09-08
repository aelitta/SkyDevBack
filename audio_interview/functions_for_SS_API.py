import requests
import http.client
import certifi
import os
import ssl
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

SS_API_KEY = os.getenv('SS_API_KEY')

custom_cert = '/Users/aelitta/Documents/salute-speech/russiantrustedca.pem' #path to Russian Cert

def get_api_token_ss():

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    custom_cert = '/Users/aelitta/Documents/salute-speech/russiantrustedca.pem' #path to Russian Cert


    payload={
    'scope': 'SALUTE_SPEECH_PERS'
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',
    'RqUID': 'e7742261-edd3-4817-933c-c20cd7d515e5',
    'Authorization': f'Basic {SS_API_KEY}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=custom_cert)

    return response.json()["access_token"]

def create_ssl_context(cert_file_path):
    """Создает SSLContext с кастомными сертификатами"""
    context = ssl.create_default_context()

    # Загружаем кастомные сертификаты
    if cert_file_path and Path(cert_file_path).exists():
        context.load_verify_locations(cert_file_path)

    # Или отключаем проверку (небезопасно!)
    # context.check_hostname = False
    # context.verify_mode = ssl.CERT_NONE

    return context

def synthesize(text):

    ssl_context = create_ssl_context(custom_cert)

    conn = http.client.HTTPSConnection("smartspeech.sber.ru", context=ssl_context)
    payload = text
    headers = {
    'Content-Type': 'application/ssml',
    'Authorization': f'Bearer {token}'
    }
    conn.request("POST", "/rest/v1/text:synthesize?format=wav16&voice=Nec_24000", payload.encode('utf-8'), headers)
    res = conn.getresponse()
    data = res.read()

    with open("hr_response.mp3", "wb") as f:
        f.write(data)

    return "hr_response.mp3"

conn = http.client.HTTPSConnection("smartspeech.sber.ru", context=ssl_context)

#распознавание
def upload_audio(path_to_audio_file):
    with open(path_to_audio_file, 'rb') as audio_file:
        # Читаем содержимое файла
        payload = audio_file.read()
    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'audio/mpeg'
    }
    conn.request("POST", "/rest/v1/data:upload", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    return data.decode("utf-8")["resut"]["request_file_id"]

#распознавание
def recognize_f(request_file_id):

    url = "https://smartspeech.sber.ru/rest/v1/speech:async_recognize"

    payload = f"{\n  \"options\": {\n    \"model\": \"general\",\n    \"audio_encoding\": \"PCM_S16LE\",\n    \"sample_rate\": 16000,\n    \"channels_count\": 1 \n  },\n  \"request_file_id\": {request_file_id}\n}' \\"

    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify = custom_cert)

    print(response.text)

    return response.text['result']['id']

#распознавание
def rec_get_status(id):
    conn = http.client.HTTPSConnection("smartspeech.sber.ru", context=ssl_context)
    payload = ''
    headers = {
    'Authorization': f'Bearer {token}'
    }
    conn.request("GET", f"/rest/v1/task:get?id={id}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    return data.decode("utf-8")['result']['response_file_id']

#распознавание
def rec_to_text(response_file_id):
    conn = http.client.HTTPSConnection("smartspeech.sber.ru", context=ssl_context)
    payload = ''
    headers = {
    'Authorization': f'Bearer {token}'
    }
    conn.request("GET",f "/rest/v1/data:download?response_file_id={response_file_id}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

    return data.decode("utf-8")[0]['results'][0]['text']

#распознавание
def recognize(path_to_audio_file):
    request_file_id = upload_audio(path_to_audio_file)
    rec_id = recognize_f(request_file_id)
    response_file_id = rec_get_status(rec_id)
    text = rec_to_text(response_file_id)

    return text