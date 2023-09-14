import requests
from translate import Translator

translator_ru = Translator(to_lang="ru", from_lang="en")
translator_en = Translator(to_lang="en", from_lang="ru")

def search_meal_by_name(name_):
    name = translator_en.translate(name_)
    print(name_, name)
    url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={name}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса

        data = response.json()
        
        if data['meals'] is None:
            print(f"Блюдо с названием '{name}' не найдено.")
        else:
            for meal in data['meals']:
                plate = f"Название блюда: { translator_ru.translate(meal['strMeal'])}"
                category = f"Категория: {translator_ru.translate(meal['strCategory'])}"
                
                text = meal['strInstructions']
                
                # Разбиваем текст на предложения
                sentences = text.split('.')
    
    # Инициализируем список для хранения переведенных предложений
                translated_sentences = []
    
    # Максимальное количество предложений в одной итерации (25)
                max_sentences_per_iteration = 3
    
                for i in range(0, len(sentences),                                 max_sentences_per_iteration):
        # Получаем подмассив предложений
                    sentences_chunk = sentences[i:i+max_sentences_per_iteration]

                    chunk_text = '.'.join(sentences_chunk)
                    
                    chunk_translation = translator_ru.translate(chunk_text)

                    translated_sentences.append(chunk_translation)

                translated_text = '.'.join(translated_sentences)
                
                #print(translated_text)
                all_text = f"{category}\nИнструкции по приготовлению:\n{translated_text}"
                return all_text, plate

    except requests.exceptions.RequestException as e:
        print("Произошла ошибка при выполнении запроса:", e)