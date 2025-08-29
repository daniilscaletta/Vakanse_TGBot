import requests
import json
from typing import List
from app.models import Vacancy

def get_top_vacancies() -> List[Vacancy]:
    
    search_text = "python"
    excluded_words = ["преподаватель", "js", "наставник", "ментор", "android"]
    specializations = ["программист", "разработчик", "DevOps", "сетевой инженер", "системный администратор", "Специалист по информационной безопасности"]
    allowed_employment_types = ["part", "project"]
    allowed_schedule_types = ["remote"]
    
    vacancies = []
    
    api_url = "https://api.hh.ru/vacancies"
    
    params = {
        'text': search_text,
        'area': '1',  # Россия
        'per_page': '100',
        'page': 0,
        'order_by': 'publication_time'  # Сортировка по дате публикации
    }
    
    headers = {
        'Accept': 'application/json',
    }
    
    try:
        print("Отправляем запрос к API hh.ru...")
        print(f"Параметры поиска: {params}")
        
        page = 0
        max_pages = 20
        
        while page < max_pages and len(vacancies) < 20:
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
                    
                    title_lower = title.lower()
                    if any(word.lower() in title_lower for word in excluded_words):
                        print(f"Пропускаем из-за исключенного слова: {title}")
                        continue
                    
                    if not any(spec.lower() in title_lower for spec in specializations):
                        print(f"Пропускаем из-за несоответствия специализации: {title}")
                        continue
                    
                    project_keywords = ['проект', 'временн', 'контракт', 'аутсорс', 'фриланс']
                    if any(keyword in title_lower for keyword in project_keywords):
                        print(f"Найдена проектная вакансия в заголовке: {title}")
                    
                    experience = item.get('experience', {}).get('id', '')
                    employment = item.get('employment', {}).get('id', '')
                    schedule = item.get('schedule', {}).get('id', '')
                    
                    if employment and employment not in allowed_employment_types:
                        print(f"Пропускаем из-за недопустимого типа занятости ({employment}): {title}")
                        continue
                    
                    if schedule and schedule not in allowed_schedule_types:
                        print(f"Пропускаем из-за недопустимого формата работы ({schedule}): {title}")
                        continue
                    
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
                    
                    vacancy = Vacancy(
                        title=title,
                        url=url,
                        salary=salary
                    )
                    
                    vacancies.append(vacancy)
                    print(f"Добавлена вакансия: {title}")
                    
                    if len(vacancies) >= 20:
                        break
                        
                except Exception as e:
                    print(f"Ошибка при обработке вакансии: {e}")
                    continue
            
            page += 1
        
        print(f"Всего найдено подходящих вакансий: {len(vacancies)}")
        
        if not vacancies:
            print("Не найдено вакансий, возвращаем заглушку")
            return
            
    except requests.RequestException as e:
        print(f"Ошибка при запросе к API hh.ru: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Ошибка при парсинге JSON: {e}")
        return
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return
    
    return vacancies