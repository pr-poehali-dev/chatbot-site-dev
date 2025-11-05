import json
import os
from typing import Dict, Any
import psycopg2
import requests

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Сохранение заявки в БД и отправка в Telegram
    Args: event - dict с httpMethod, body (name, telegram, niche)
    Returns: HTTP response с результатом
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
    name: str = body.get('name', '')
    telegram: str = body.get('telegram', '')
    niche: str = body.get('niche', '')
    
    if not all([name, telegram, niche]):
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'isBase64Encoded': False,
            'body': json.dumps({'error': 'Missing required fields'})
        }
    
    try:
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO leads (name, telegram, niche, created_at)
            VALUES (%s, %s, %s, NOW())
            RETURNING id
        """, (name, telegram, niche))
        lead_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'isBase64Encoded': False,
            'body': json.dumps({'error': 'Database error'})
        }
    
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHAT_ID')
    
    if bot_token and chat_id:
        message = f"🆕 Новая заявка #{lead_id}\n\n👤 Имя: {name}\n✉️ Telegram: {telegram}\n💼 Ниша: {niche}"
        
        try:
            requests.post(
                f'https://api.telegram.org/bot{bot_token}/sendMessage',
                json={
                    'chat_id': chat_id,
                    'text': message,
                    'parse_mode': 'HTML'
                },
                timeout=5
            )
        except:
            pass
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'isBase64Encoded': False,
        'body': json.dumps({'success': True, 'id': lead_id})
    }
