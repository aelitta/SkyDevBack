def run(in_params={query: str, mp3_path: str}):
    outparams = {}

    import requests
    from SkyDevBack.audio_interview.functions_for_SS_API import * #загружаем функции для синтеза и распознавания
    from dotenv import load_dotenv


    load_dotenv()

    OPEN_ROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')
    API_URL = 'https://openrouter.ai/api/v1/chat/completions'

    query = in_params['query']

    # Define the headers for the API request to DeepSeek
    headers = {
        'Authorization': f'Bearer {OPEN_ROUTER_API_KEY}',
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


    hr_resp = synthesize(q) #первый вопрос отправить кандидату, оборачиваем в голос

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
    #в цикле прокручиваем диалог
    while cand_resp.lower().find('всего доброго')<0 and cand_resp.lower().find('до свидания')<0 \
        and hr_resp.find('кандидат')<0 and cand_resp.lower().find('пока')<0 and cand_resp.lower().find('всего хорошего')
        and len(cand_resp)>0:

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

        messages.append({
            "role": "assistant",
            "content": q
            })

        messages.append({
            "role": "user",
            "content": cand_resp
            })


    outparams["interview_text"] = messages
    outparams['mp3_path'] = in_params['mp3_path']
    outparams["def"] = 'Audio Interview'

    return outparams
