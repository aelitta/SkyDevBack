import requests
import selenium
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
import os
import sys

from deepseek_python_similarity_metrics import TextNormalizer, TextSimilarityCalculator


# browser = webdriver.Firefox()
# browser.get(pg)

keywords = 'бизнес-аналитик, Москва, банк, противодействие мошенничеству, антифрод, платежные карты, ДБО, корпоративные карты, бизнес-требования, функциональные требования, СУБД, техническая документация, ПОД/ФТ, риск-менеджмент'
keywords = keywords.split(',')

def get_cvs(keywords, folder_path):
    browser = webdriver.Firefox()
    browser.get(pg)
    # text = 'бизнес-аналитик, Москва, банк, противодействие мошенничеству, антифрод, платежные карты, ДБО, корпоративные карты, бизнес-требования, функциональные требования, СУБД, техническая документация, ПОД/ФТ, риск-менеджмент'
    text = '+'.join(keywords).replace('+ ','+')

    pg = f'https://hh.ru/search/resume?text={text}&logic=normal&pos=full_text&exp_period=all_time&exp_company_size=any&filter_exp_period=all_time&area=1&relocation=living_or_relocation&age_from=&age_to=&gender=unknown&salary_from=&salary_to=&currency_code=RUR&order_by=relevance&search_period=0&items_on_page=1000&hhtmFrom=resume_search_form'
    records_fetched=0
    browser.get(pg)

    soup = BeautifulSoup(browser.page_source, "lxml")

    for a in soup.find_all("a", attrs={"data-qa": "serp-item__title"}):
        res = f"https://hh.ru{a.attrs['href'].split('?')[0]}"
        browser.get(res)
        page_text = browser.find_element(By.TAG_NAME, "body").text
        filename = f"{folder_path}/res{records_fetched+1}.txt"

        # Open the file in write mode with UTF-8 encoding
        with open(filename, "w", encoding="utf-8") as file:
            # Write the page source to the file
            file.write(page_text)
        records_fetched += 1

    return records_fetched

folder_path = '/Users/aelitta/Documents/salute-speech/biznes-analitik'
# records_fetched = get_cvs(keywords, folder_path)
records_fetched = 20
if records_fetched<100:
    keywords1 = keywords[:len(keywords)//2]
    records_fetched = records_fetched+get_cvs(keywords1, folder_path)
if records_fetched<100:
    keywords1 = keywords[len(keywords)//2:]
    records_fetched = records_fetched+get_cvs(keywords1, folder_path)
if records_fetched<100:
    keywords1 = keywords[:1]
    records_fetched = records_fetched+get_cvs(keywords1, folder_path)




def get_similarity(file_pat, vacancy_txt_file):
    calculator = TextSimilarityCalculator()
    sim_dict = {}
    for res in os.listdir(folder_path):
        try:
            # Базовый расчет схожести
            similarity = calculator.calculate_similarity(vacancy_txt_file, f"{folder_path}/{res}")
            sim_dict[res] = similarity
            # print(f"\nМера похожести после нормализации: {similarity:.4f}")
            # print(f"Процент совпадения: {similarity * 100:.2f}%")

            # Детальный анализ
            analysis = calculator.get_detailed_analysis(vacancy_txt_file, f"{folder_path}/{res}")
            # print(f"\nДетальный анализ:")
            # print(f"Общих слов: {analysis['common_words_count']}")
            # print(f"Уникальных слов в вакансии: {analysis['vacancy_word_count']}")
            # print(f"Уникальных слов в резюме: {analysis['resume_word_count']}")
            # print(f"Топ общих слов: {', '.join(analysis['common_words'])}")

        except FileNotFoundError as e:
            print(f"Ошибка: Файл не найден - {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    return sim_dict
