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
    
    messages = [{'role': 'system', 'content': system_prompt}]
    for msg in chat_history:
        if msg['role'] in ['user', 'assistant']:
            messages.append({'role': msg['role'], 'content': msg['content']})
    
    messages.append({'role': 'user', 'content': user_message})
    
    vsegpt_key = os.environ.get('VSEGPT_API_KEY')
    
    try:
        vsegpt_response = requests.post(
            'https://api.vsegpt.ru/v1/chat/completions',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {vsegpt_key}'
            },
            json={
                'model': 'openai/gpt-4o-mini',
                'messages': messages,
                'temperature': 0.7,
                'max_tokens': 300
            },
            timeout=15
        )
        
        result = vsegpt_response.json()
        reply = result['choices'][0]['message']['content']
        
    except:
        reply = "Привет! Я AI-консультант по Telegram-ботам. Расскажите, чем занимаетесь и какие задачи хотите автоматизировать?"
    
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