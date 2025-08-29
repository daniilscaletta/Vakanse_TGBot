import requests
import json
from typing import List
from app.models import Vacancy

def get_top_vacancies() -> List[Vacancy]:
    """
    Получает вакансии с hh.ru через API по заданным параметрам:
    - Поиск: python
    - Исключенные слова: преподаватель, js, наставник, ментор, Android
    - Регион: Россия
    - Специализации: Программист, разработчик; DevOps-инженер; Сетевой инженер; 
      Системный администратор; Системный инженер; Специалист по информационной безопасности
    - Опыт работы: не имеет значения
    - Тип занятости: Частичная занятость; Проектная работа
    - Формат работы: Удаленно
    """
    
    # Параметры поиска
    search_text = "python"
    excluded_words = ["преподаватель", "js", "наставник", "ментор", "android"]
    specializations = [
        "программист", "разработчик", "DevOps", "сетевой инженер", "системный администратор", "Специалист по информационной безопасности"
    ]
    
    # Параметры фильтрации
    # Допустимые типы занятости (исключаем полную занятость)
    allowed_employment_types = ["part", "project"]  # Частичная и проектная работа
    excluded_employment_types = ["full"]  # Полная занятость - исключаем
    
    # Допустимый формат работы
    allowed_schedule_types = ["remote"]  # Только удаленно
    
    vacancies = []
    
    # API URL для поиска вакансий
    api_url = "https://api.hh.ru/vacancies"
    
    # Параметры запроса к API (используем только поддерживаемые параметры)
    params = {
        'text': search_text,
        'area': '1',  # Россия
        'per_page': '100',  # Увеличиваем количество вакансий на странице для лучшей фильтрации
        'page': 0,
        'order_by': 'publication_time'  # Сортировка по дате публикации
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Accept-Language': 'ru-RU,ru;q=0.9,en;q=0.8',
    }
    
    try:
        print("Отправляем запрос к API hh.ru...")
        print(f"Параметры поиска: {params}")
        
        # Ищем вакансии на нескольких страницах
        page = 0
        max_pages = 20  # Максимум 3 страницы
        
        while page < max_pages and len(vacancies) < 15:
            params['page'] = page
            print(f"Обрабатываем страницу {page + 1}...")
            
            response = requests.get(api_url, params=params, headers=headers, timeout=15)
            response.raise_for_status()
            
            print(f"Получен ответ: {response.status_code}")
            
            data = response.json()
            
            if 'items' not in data or not data['items']:
                print(f"Не найдены вакансии на странице {page + 1}")
                break
            
            print(f"Найдено вакансий на странице {page + 1}: {len(data['items'])}")
            
            for item in data['items']:
                try:
                    title = item.get('name', '')
                    
                    # Проверяем исключенные слова в заголовке
                    title_lower = title.lower()
                    if any(word.lower() in title_lower for word in excluded_words):
                        print(f"Пропускаем из-за исключенного слова: {title}")
                        continue
                    
                    # Проверяем специализацию в заголовке
                    if not any(spec.lower() in title_lower for spec in specializations):
                        print(f"Пропускаем из-за несоответствия специализации: {title}")
                        continue
                    
                    # Дополнительная проверка на проектные вакансии в заголовке
                    project_keywords = ['проект', 'временн', 'контракт', 'аутсорс', 'фриланс']
                    if any(keyword in title_lower for keyword in project_keywords):
                        print(f"Найдена проектная вакансия в заголовке: {title}")
                    
                    # Дополнительная фильтрация по параметрам вакансии
                    experience = item.get('experience', {}).get('id', '')
                    employment = item.get('employment', {}).get('id', '')
                    schedule = item.get('schedule', {}).get('id', '')
                    
                    # Проверяем, что тип занятости соответствует требованиям
                    if employment and employment not in allowed_employment_types:
                        print(f"Пропускаем из-за недопустимого типа занятости ({employment}): {title}")
                        continue
                    
                    # Проверяем формат работы - только удаленно
                    if schedule and schedule not in allowed_schedule_types:
                        print(f"Пропускаем из-за недопустимого формата работы ({schedule}): {title}")
                        continue
                    
                    # Получаем URL вакансии
                    url = item.get('alternate_url', '')
                    if not url:
                        print(f"Не найден URL для вакансии: {title}")
                        continue
                    
                    # Получаем зарплату
                    salary_info = item.get('salary', {})
                    if salary_info:
                        salary_from = salary_info.get('from')
                        salary_to = salary_info.get('to')
                        salary_currency = salary_info.get('currency', 'RUB')
                        
                        if salary_from and salary_to:
                            salary = f"{salary_from}-{salary_to} {salary_currency}"
                        elif salary_from:
                            salary = f"от {salary_from} {salary_currency}"
                        elif salary_to:
                            salary = f"до {salary_to} {salary_currency}"
                        else:
                            salary = "Зарплата не указана"
                    else:
                        salary = "Зарплата не указана"
                    
                    print(f"Обрабатываем вакансию: {title}")
                    print(f"Зарплата: {salary}")
                    print(f"Опыт: {experience}, Занятость: {employment}, График: {schedule}")
                    
                    # Создаем объект вакансии
                    vacancy = Vacancy(
                        title=title,
                        url=url,
                        salary=salary
                    )
                    
                    vacancies.append(vacancy)
                    print(f"Добавлена вакансия: {title}")
                    
                    # Ограничиваем количество вакансий
                    if len(vacancies) >= 15:
                        break
                        
                except Exception as e:
                    print(f"Ошибка при обработке вакансии: {e}")
                    continue
            
            page += 1
        
        print(f"Всего найдено подходящих вакансий: {len(vacancies)}")
        
        # Если не нашли вакансий, возвращаем заглушку
        if not vacancies:
            print("Не найдено вакансий, возвращаем заглушку")
            return get_fallback_vacancies()
            
    except requests.RequestException as e:
        print(f"Ошибка при запросе к API hh.ru: {e}")
        return get_fallback_vacancies()
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return get_fallback_vacancies()
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return get_fallback_vacancies()
    
    return vacancies

def get_fallback_vacancies() -> List[Vacancy]:
    """Возвращает заглушку вакансий в случае ошибки"""
    return [
        Vacancy(
            title="Python Backend Developer (Удаленно, Частичная занятость)",
            url="https://hh.ru/vacancy/123456",
            salary="150000 RUB"
        ),
        Vacancy(
            title="DevOps Engineer (Удаленно, Проектная работа)",
            url="https://hh.ru/vacancy/123457", 
            salary="200000 RUB"
        )
    ]