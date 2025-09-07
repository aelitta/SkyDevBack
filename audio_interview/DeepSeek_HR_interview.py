#Подключаемся к DeepSeek

import requests
from functions_for_SS_API import *

# Replace with your OpenRouter API key
API_KEY = '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'
API_URL = 'https://openrouter.ai/api/v1/chat/completions'

query = 'бизнес-аналитик'

# Define the headers for the API request
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

# Define the request payload (data)
data = {
    "model": "deepseek/deepseek-chat-v3.1:free",
    "messages": [
        {
      "role": "system",
      "content": f"Ты — HR-специалист, проводящий собеседование на позицию {query} в сфере противодействия мошенничеству (антифрод). Кандидат имеет опыт в банковской сфере, работу с процессинговыми системами (в т.ч. Way4), знание SQL и опыт анализа требований. Задавай вопросы по одному. Будь профессиональным и дружелюбным."
        }
    ]
        # {"role": "user", "content": f"Please translate {query} to English, return only translation"}]
}

# Send the POST request to the DeepSeek API
response = requests.post(API_URL, json=data, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    q = response.json()['choices'][0]['message']['content']
else:
    print("Failed to fetch data from API. Status Code:", response.status_code)


hr_resp = synthesize(q) #первый вопрос отправить кандидату

#получаем аудио от кандидата

cand_resp = recognize(path_to_audio)

messages = [{
      "role": "system",
      "content": f"Ты — HR-специалист, проводящий собеседование на позицию {query} в сфере противодействия мошенничеству (антифрод). Кандидат имеет опыт в банковской сфере, работу с процессинговыми системами (в т.ч. Way4), знание SQL и опыт анализа требований. Задавай вопросы по одному. Будь профессиональным и дружелюбным."
        },
        {
      "role": "assistant",
      "content": q
      },
      {
      "role": "user",
      "content": cand_resp
      }
]

while cand_resp.lower().find('всего доброго')<0 and cand_resp.lower().find('до свидания')<0 \
    and hr_resp.find('кандидат')<0:

    data = {
        "model": "deepseek/deepseek-chat-v3.1:free",
        "messages": messages
            # {"role": "user", "content": f"Please translate {query} to English, return only translation"}]
    }

    response = requests.post(API_URL, json=data, headers=headers)
        if response.status_code == 200:
            q = response.json()['choices'][0]['message']['content']
        else:
            print("Failed to fetch data from API. Status Code:", response.status_code)


        hr_resp = synthesize(q) #первый вопрос отправить кандидату

        #получаем аудио от кандидата

        cand_resp = recognize(path_to_audio)


print(messages)