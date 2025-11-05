import json
import os
from typing import Dict, Any, List
import psycopg2
from openai import OpenAI

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
    
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
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

Если собрал имя, telegram и нишу - предложи оставить заявку и попрощайся.
"""
    
    messages = [{'role': 'system', 'content': system_prompt}]
    
    for msg in chat_history:
        messages.append({
            'role': msg['role'],
            'content': msg['content']
        })
    
    messages.append({'role': 'user', 'content': user_message})
    
    completion = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=messages,
        temperature=0.7,
        max_tokens=300
    )
    
    reply = completion.choices[0].message.content
    
    if not user_data.get('name') and any(word in user_message.lower() for word in ['меня зовут', 'я ', 'имя']):
        words = user_message.split()
        for i, word in enumerate(words):
            if word.lower() in ['зовут', 'я'] and i + 1 < len(words):
                user_data['name'] = words[i + 1].strip('.,!?')
                break
    
    if not user_data.get('telegram') and ('@' in user_message or 'telegram' in user_message.lower()):
        parts = user_message.split()
        for part in parts:
            if part.startswith('@'):
                user_data['telegram'] = part
                break
    
    if not user_data.get('niche'):
        niches = ['салон', 'школа', 'магазин', 'агентство', 'консультант', 'эксперт', 'услуг']
        for niche in niches:
            if niche in user_message.lower():
                user_data['niche'] = user_message
                break
    
    if all([user_data.get('name'), user_data.get('telegram'), user_data.get('niche')]):
        try:
            conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO leads (name, telegram, niche, created_at)
                VALUES (%s, %s, %s, NOW())
            """, (user_data['name'], user_data['telegram'], user_data['niche']))
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
