import json
import os
import re
from typing import Dict, Any, List
import psycopg2
import requests

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: AI чат-бот консультант для продажи ботов и сбора заявок
    Args: event - dict с message, messages, userData
    Returns: HTTP response с reply и обновленными userData
    '''
    method: str = event.get('httpMethod', 'POST')
    
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '86400'
            },
            'body': ''
        }
    
    body = json.loads(event.get('body', '{}'))
    user_message: str = body.get('message', '')
    chat_history: List[Dict] = body.get('messages', [])
    user_data: Dict = body.get('userData', {})
    
    system_prompt = """Ты AI-консультант по автоматизации бизнеса через Telegram-ботов и AI-агентов.

Твоя задача:
1. Понять нишу клиента и его боли
2. Предложить подходящее решение (бот для записи, AI-консультант, интеграция с CRM и т.д.)
3. Собрать контакты: имя, Telegram, ниша бизнеса
4. Мотивировать оставить заявку

Стиль общения:
- Дружелюбный и профессиональный
- Короткие сообщения (2-3 предложения)
- Задавай уточняющие вопросы
- Покажи выгоду и результаты

Если собрал имя, telegram и нишу - предложи оставить заявку и попрощайся."""
    
    messages = []
    for msg in chat_history:
        if msg['role'] == 'user':
            messages.append({'role': 'user', 'text': msg['content']})
        elif msg['role'] == 'assistant':
            messages.append({'role': 'assistant', 'text': msg['content']})
    
    messages.append({'role': 'user', 'text': user_message})
    
    api_key = os.environ.get('YANDEX_API_KEY')
    folder_id = os.environ.get('YANDEX_FOLDER_ID')
    
    try:
        yandex_response = requests.post(
            'https://llm.api.cloud.yandex.net/foundationModels/v1/completion',
            headers={
                'Authorization': f'Api-Key {api_key}',
                'Content-Type': 'application/json'
            },
            json={
                'modelUri': f'gpt://{folder_id}/yandexgpt-lite/latest',
                'completionOptions': {
                    'stream': False,
                    'temperature': 0.7,
                    'maxTokens': 300
                },
                'messages': [
                    {'role': 'system', 'text': system_prompt}
                ] + messages
            },
            timeout=30
        )
        
        result = yandex_response.json()
        
        if 'result' in result:
            reply = result['result']['alternatives'][0]['message']['text']
        elif 'error' in result:
            reply = f"Извините, возникла ошибка: {result['error'].get('message', 'неизвестная ошибка')}"
        else:
            reply = "Извините, не могу ответить сейчас. Попробуйте позже или напишите напрямую."
    except Exception as e:
        reply = f"Извините, сервис временно недоступен. Напишите мне напрямую в Telegram!"
    
    if not user_data.get('name'):
        name_patterns = [
            r'(?:меня зовут|я\s+)([А-ЯЁа-яё]+)',
            r'^([А-ЯЁ][а-яё]+)$'
        ]
        for pattern in name_patterns:
            match = re.search(pattern, user_message)
            if match:
                user_data['name'] = match.group(1).capitalize()
                break
    
    if not user_data.get('telegram'):
        telegram_patterns = [
            r'@(\w+)',
            r't\.me/(\w+)',
            r'telegram:\s*@?(\w+)'
        ]
        for pattern in telegram_patterns:
            match = re.search(pattern, user_message, re.IGNORECASE)
            if match:
                user_data['telegram'] = '@' + match.group(1).lstrip('@')
                break
    
    if not user_data.get('niche'):
        niches = {
            'салон': ['салон', 'красот', 'маникюр', 'парикмахер', 'барбер'],
            'онлайн-школа': ['школ', 'курс', 'обучени', 'образован', 'тренинг'],
            'магазин': ['магазин', 'продаж', 'товар'],
            'агентство': ['агентство', 'маркетинг'],
            'консультант': ['консультант', 'эксперт', 'коуч']
        }
        for niche_name, keywords in niches.items():
            if any(kw in user_message.lower() for kw in keywords):
                user_data['niche'] = niche_name
                break
    
    if all([user_data.get('name'), user_data.get('telegram')]):
        try:
            conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO leads (name, telegram, niche, created_at)
                VALUES (%s, %s, %s, NOW())
                ON CONFLICT DO NOTHING
            """, (user_data['name'], user_data['telegram'], user_data.get('niche', 'не указана')))
            conn.commit()
            cur.close()
            conn.close()
        except Exception:
            pass
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'isBase64Encoded': False,
        'body': json.dumps({
            'reply': reply,
            'userData': user_data
        }, ensure_ascii=False)
    }