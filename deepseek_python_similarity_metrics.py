import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import nltk
from typing import List, Dict, Set
import string

# Скачиваем необходимые ресурсы NLTK
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

class TextNormalizer:
    def __init__(self):
        # Словари для нормализации
        self.russian_stopwords = set(stopwords.words('russian'))
        self.english_stopwords = set(stopwords.words('english'))
        self.all_stopwords = self.russian_stopwords.union(self.english_stopwords)
        
        # Инициализация стеммеров и лемматизаторов
        self.russian_stemmer = SnowballStemmer('russian')
        self.english_stemmer = SnowballStemmer('english')
        self.lemmatizer = WordNetLemmatizer()
        
        # Словарь для замены синонимов и аббревиатур
        self.synonyms = {
            'js': 'javascript', 'react.js': 'react', 'vue.js': 'vue',
            'ml': 'машинное обучение', 'ai': 'искусственный интеллект',
            'devops': 'development operations', 'ci/cd': 'continuous integration',
            'sql': 'structured query language', 'nosql': 'not only sql',
            'oop': 'объектно ориентированное программирование',
            'фронтенд': 'frontend', 'бэкенд': 'backend', 'фуллстек': 'fullstack',
            'пхп': 'php', 'питон': 'python', 'джава': 'java',
            'с++': 'cplusplus', 'c#': 'csharp'
        }
        
        # Словарь для нормализации навыков
        self.skills_normalization = {
            'python': ['python', 'питон', 'пайтон'],
            'java': ['java', 'джава'],
            'javascript': ['javascript', 'js', 'джаваскрипт'],
            'sql': ['sql', 'structured query language'],
            'html': ['html', 'htm'],
            'css': ['css'],
            'react': ['react', 'react.js', 'reactjs'],
            'vue': ['vue', 'vue.js', 'vuejs'],
            'angular': ['angular', 'angular.js', 'angularjs'],
            'docker': ['docker'],
            'kubernetes': ['kubernetes', 'k8s'],
            'aws': ['aws', 'amazon web services'],
            'azure': ['azure', 'microsoft azure'],
            'gcp': ['gcp', 'google cloud platform']
        }

    def normalize_text(self, text: str) -> str:
        """Полная нормализация текста"""
        text = self._clean_text(text)
        text = self._replace_synonyms(text)
        text = self._normalize_skills(text)
        text = self._remove_stopwords(text)
        text = self._lemmatize_text(text)
        return text

    def _clean_text(self, text: str) -> str:
        """Очистка текста от мусора"""
        # Приведение к нижнему регистру
        text = text.lower()
        
        # Удаление email-адресов
        text = re.sub(r'\S+@\S+', ' ', text)
        
        # Удаление URL
        text = re.sub(r'http\S+', ' ', text)
        
        # Удаление телефонных номеров
        text = re.sub(r'\+?[7-8]?[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}', ' ', text)
        
        # Удаление специальных символов, кроме букв и пробелов
        text = re.sub(r'[^a-zA-Zа-яА-ЯёЁ\s]', ' ', text)
        
        # Удаление лишних пробелов
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def _replace_synonyms(self, text: str) -> str:
        """Замена синонимов и аббревиатур"""
        for synonym, replacement in self.synonyms.items():
            text = re.sub(r'\b' + re.escape(synonym) + r'\b', replacement, text)
        return text

    def _normalize_skills(self, text: str) -> str:
        """Нормализация названий технологий и навыков"""
        for normalized, variants in self.skills_normalization.items():
            pattern = r'\b(' + '|'.join(map(re.escape, variants)) + r')\b'
            text = re.sub(pattern, normalized, text)
        return text

    def _remove_stopwords(self, text: str) -> str:
        """Удаление стоп-слов"""
        tokens = word_tokenize(text)
        filtered_tokens = [token for token in tokens if token not in self.all_stopwords and len(token) > 2]
        return ' '.join(filtered_tokens)

    def _lemmatize_text(self, text: str) -> str:
        """Лемматизация текста"""
        tokens = word_tokenize(text)
        lemmatized_tokens = []
        
        for token in tokens:
            # Пробуем лемматизировать как английское слово
            try:
                lemmatized = self.lemmatizer.lemmatize(token)
                if lemmatized != token:
                    lemmatized_tokens.append(lemmatized)
                else:
                    # Если лемматизация не изменила слово, используем стемминг
                    if any(cyrillic in token for cyrillic in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'):
                        lemmatized_tokens.append(self.russian_stemmer.stem(token))
                    else:
                        lemmatized_tokens.append(self.english_stemmer.stem(token))
            except:
                lemmatized_tokens.append(token)
        
        return ' '.join(lemmatized_tokens)

class TextSimilarityCalculator:
    def __init__(self):
        self.normalizer = TextNormalizer()
    
    def read_file(self, file_path: str) -> str:
        """Чтение файла с обработкой разных кодировок"""
        encodings = ['utf-8', 'cp1251', 'iso-8859-1', 'windows-1252']
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
        
        raise ValueError(f"Не удалось прочитать файл {file_path} с поддерживаемыми кодировками")
    
    def calculate_similarity(self, vacancy_path: str, resume_path: str) -> float:
        """Расчет меры похожести с нормализацией"""
        # Чтение файлов
        vacancy_text = self.read_file(vacancy_path)
        resume_text = self.read_file(resume_path)
        k = resume_text.find('Кандидат')
        resume_text = resume_text[k+8:]
        
        # Нормализация текстов
        normalized_vacancy = self.normalizer.normalize_text(vacancy_text)
        normalized_resume = self.normalizer.normalize_text(resume_text)
        
        print("Нормализованное описание вакансии:")
        print(normalized_vacancy[:500] + "..." if len(normalized_vacancy) > 500 else normalized_vacancy)
        print("\nНормализованное резюме:")
        print(normalized_resume[:500] + "..." if len(normalized_resume) > 500 else normalized_resume)
        
        # Создание TF-IDF векторов
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=1000)
        tfidf_matrix = vectorizer.fit_transform([normalized_vacancy, normalized_resume])
        
        # Расчет косинусного сходства
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        
        return similarity
    
    def get_detailed_analysis(self, vacancy_path: str, resume_path: str) -> Dict:
        """Детальный анализ с нормализацией"""
        vacancy_text = self.read_file(vacancy_path)
        resume_text = self.read_file(resume_path)
        k = resume_text.find('Кандидат')
        resume_text = resume_text[k+8:]
        
        # Нормализация
        norm_vacancy = self.normalizer.normalize_text(vacancy_text)
        norm_resume = self.normalizer.normalize_text(resume_text)
        
        # Анализ общих слов
        vacancy_words = set(norm_vacancy.split())
        resume_words = set(norm_resume.split())
        common_words = vacancy_words.intersection(resume_words)
        
        # Расчет схожести
        similarity = self.calculate_similarity(vacancy_path, resume_path)
        
        return {
            'similarity_score': similarity,
            'common_words_count': len(common_words),
            'common_words': list(common_words)[:20],  # Первые 20 общих слов
            'vacancy_word_count': len(vacancy_words),
            'resume_word_count': len(resume_words),
            'normalized_vacancy': norm_vacancy,
            'normalized_resume': norm_resume
        }

# Пример использования
def main():
    calculator = TextSimilarityCalculator()
    i=5
    
    try:
        # Базовый расчет схожести
        similarity = calculator.calculate_similarity("/Users/aelitta/Documents/salute-speech/AI HR/бизнес-аналитик.txt", f"/Users/aelitta/Documents/salute-speech/biznes-analitik/res{i}.txt")
        print(f"\nМера похожести после нормализации: {similarity:.4f}")
        print(f"Процент совпадения: {similarity * 100:.2f}%")
        
        # Детальный анализ
        analysis = calculator.get_detailed_analysis("/Users/aelitta/Documents/salute-speech/AI HR/бизнес-аналитик.txt", f"/Users/aelitta/Documents/salute-speech/biznes-analitik/res{i}.txt")
        print(f"\nДетальный анализ:")
        print(f"Общих слов: {analysis['common_words_count']}")
        print(f"Уникальных слов в вакансии: {analysis['vacancy_word_count']}")
        print(f"Уникальных слов в резюме: {analysis['resume_word_count']}")
        print(f"Топ общих слов: {', '.join(analysis['common_words'])}")
        
    except FileNotFoundError as e:
        print(f"Ошибка: Файл не найден - {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    main()
