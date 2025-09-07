import sys
import pandas as pd
# sys.path.append('/Users/aelitta/Documents/salute-speech') #путь к функциям похожести
from deepseek_python_similarity_metrics import TextNormalizer, TextSimilarityCalculator
from dotenv import load_dotenv

load_dotenv()

OPEN_ROUTER_API_KEY = os.getenv('OPEN_ROUTER_API_KEY')

folder_path = '/Users/aelitta/Documents/salute-speech/biznes-analitik'



def extract_txt_file(file_path):
    # Чтение TXT файла
    with open(file_path, 'r', encoding='utf-8') as file:
        text_content = file.read()

    # Обрезаем текст если слишком длинный (ограничение контекста)
    max_length = 10000  # подстройте под вашу модель
    if len(text_content) > max_length:
        text_content = text_content[:max_length]

    return text_content

def get_similarity_by_hard_skills(folder_path, skills):

    calculator = TextSimilarityCalculator()
    sim_dict = {}

    # Текст из файла
    for res in os.listdir(folder_path):
        file_text = extract_txt_file(folder_path+'/'+res)



        # Запрос к OpenRouter
        API_KEY = OPEN_ROUTER_API_KEY
        API_URL = 'https://openrouter.ai/api/v1/chat/completions'
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "deepseek/deepseek-chat-v3.1:free",
            "max_tokens" : 300,
            "messages": [
                {
                    "role": "user",
                    "content": f"Проанализируй этот документ и выдели hard skills, опыт и образование кандидатов:\n\n{file_text}, выведи только hard skills, опыт и образование"
                }
            ]
        }
        response = requests.post(API_URL, json=data, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            print("API Response:", response.json())
        else:
            print("Failed to fetch data from API. Status Code:", response.status_code)

        result = response.json()

        similarity = calculator.calculate_similarity_text(skills, result['choices'][0]['message']['content'])
        sim_dict[res] = similarity

    return sim_dict

sim_dict = get_similarity_by_hard_skills(folder_path, skills)
pd.DataFrame.from_dict(sim_dict, orient='index').sort_values(by = 0, ascending = False) #сортировка таблицы