import json
import os
import re
from typing import Dict, Any, List
import psycopg2

def generate_smart_reply(user_message: str, user_data: Dict, message_count: int) -> str:
    '''Генерирует умный ответ на основе контекста'''
    msg_lower = user_message.lower()
    
    if message_count == 1:
        if any(word in msg_lower for word in ['салон', 'красот', 'маникюр', 'парикмахер']):
            return "Отлично! Для салонов красоты я создаю ботов для автоматической записи. Клиенты сами выбирают мастера, услугу и время — без звонков менеджеру. Хотите, расскажу подробнее?"
        elif any(word in msg_lower for word in ['школ', 'курс', 'обучени', 'образован']):
            return "Супер! Для онлайн-школ делаю ботов с автозаписью на курсы, приемом оплаты и выдачей доступов. Ученики получают всё автоматически. Интересно?"
        elif any(word in msg_lower for word in ['магазин', 'продаж', 'товар', 'интернет-магазин']):
            return "Здорово! Могу сделать AI-консультанта для вашего магазина — он подбирает товары, отвечает на вопросы и оформляет заказы. До 70% запросов обрабатывает без менеджера. Расскажу больше?"
        else:
            return "Интересно! Расскажите подробнее, чем занимаетесь? Какие задачи хотите автоматизировать?"
    
    if 'да' in msg_lower or 'интересно' in msg_lower or 'расскажи' in msg_lower:
        return "Отлично! Процесс простой: вы оставляете заявку → я готовлю сценарий работы бота → запускаем за 3-7 дней. Как вас зовут?"
    
    if not user_data.get('name'):
        return "Приятно познакомиться! А как с вами связаться? Укажите ваш Telegram, пожалуйста."
    
    if not user_data.get('telegram'):
        return "Отлично! Я свяжусь с вами в ближайшее время и подготовлю индивидуальное предложение. Ожидайте сообщение в Telegram!"
    
    return "Спасибо за заявку! Скоро свяжусь с вами в Telegram и обсудим детали. До скорой встречи! 👋"

def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    '''
    Business: Чат-бот консультант для продажи ботов и сбора заявок
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
    
    message_count = len([m for m in chat_history if m['role'] == 'user']) + 1
    
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
    
    reply = generate_smart_reply(user_message, user_data, message_count)
    
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
