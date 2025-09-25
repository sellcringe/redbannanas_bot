import re
from datetime import datetime, timedelta

import requests
import json

from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.db.models import Auth


def get_data_by_webhook(webhook_data: dict):
    # webhook_data = {
    #     'event': 'ONCRMDYNAMICITEMUPDATE',
    #     'event_handler_id': '1165',
    #     'data[FIELDS][ID]': '4',
    #     'data[FIELDS][ENTITY_TYPE_ID]': '1088',
    #     'ts': '1758613539',
    #     'auth[domain]': 'rbbase.ru',
    #     'auth[client_endpoint]': 'https://rbbase.ru/rest/',
    #     'auth[server_endpoint]': 'https://oauth.bitrix24.tech/rest/',
    #     'auth[member_id]': '0b4604116f95c18eb130d88b298001ee',
    #     'auth[application_token]': 'oqegyd0ujo2u8a7srodd39znpqiny4jg'
    # }

    # Формируем URL для REST API вызова
    member_id = webhook_data['auth[member_id]']
    app_token = webhook_data['auth[application_token]']
    method = "crm.item.get"  # Универсальный метод для получения элемента CRM

    rest_url = f"https://rbbase.ru/rest/{member_id}/{app_token}/{method}"
    rest_url = 'https://rbbase.ru/rest/244/th59hcc5qids1hkp/crm.item.get'
    headers = {
        # "Content - Type": "application / json",
        'Content-Type': 'application/json'
    }
    # Параметры для запроса: ID элемента и ID типа сущности
    entity_type_id = webhook_data['data[FIELDS][ENTITY_TYPE_ID]']  # 1088
    item_id = webhook_data['data[FIELDS][ID]']  # 4

    params = {
        'entityTypeId': entity_type_id,
        'id': item_id
    }

    # Отправляем запрос
    response = requests.post(rest_url, data=json.dumps(params), headers=headers)

    if response.status_code == 200:
        result = response.json()
        if 'result' in result:
            # Вот полные данные об элементе
            item_data = result['result']
            print("Данные элемента:", json.dumps(item_data, indent=2, ensure_ascii=False))
        else:
            print("Ошибка в запросе:", result.get('error_description', 'Unknown error'))
    else:
        print("HTTP ошибка:", response.status_code)
        print(response.content)




def get_smart_proccess_by_date():
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    # Форматируем даты для фильтра (без времени)
    yesterday_start = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_end = yesterday.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Конвертируем в строку для Bitrix24
    yesterday_start_str = yesterday_start.strftime('%Y-%m-%dT%H:%M:%S%z')
    yesterday_end_str = yesterday_end.strftime('%Y-%m-%dT%H:%M:%S%z')
    url = 'https://rbbase.ru/rest/244/th59hcc5qids1hkp/crm.item.list'
    headers = {
        'Content-Type': 'application/json'
    }
    date = "ufCrm31_1758200099"
    params = {
        'entityTypeId': 1088,  # ID вашего Smart-процесса
        'select': ['id', 'title',"ufCrm31_1758200144", date, "ufCrm31_1758624931"],
        'filter': {
            '>=ufCrm31_1758200099': yesterday_start_str,
            '<=ufCrm31_1758200099': yesterday_end_str
        },
        # поля для выборки,


    }
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(params))
    # response =
    # for item in json.loads(response.content)['result']['items']:
    #     print(item)
    return json.loads(response.content)


def test():
    url = 'https://rbbase.ru/rest/244/th59hcc5qids1hkp/crm.item.fields'
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'entityTypeId': 1088,  # ID вашего Smart-процесса
        # 'select': ['id', 'title', 'stageId', 'createdTime', 'assignedById']  # поля для выборки
    }
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(params))
    response = json.loads(response.content)
    print(response)
    for item in response['result']['items']:
        print(item)



async def get_userid_by_username(username: str, sessionmaker: async_sessionmaker):
    username = extract_username(username)
    async with sessionmaker() as session:
        async with session.begin():

            result: ScalarResult = await session.scalars(select(Auth).where(
                Auth.username == username
            ))
            user: Auth = result.one_or_none()
            print(user)
            if user is None:
                return False

            return user.user_id


def extract_username(text: str) -> str:
    """
    Извлекает username из различных форматов:
    - https://t.me/sellcringe -> sellcringe
    - @sellcringe -> sellcringe
    - t.me/sellcringe -> sellcringe
    - sellcringe -> sellcringe
    """
    # Удаляем все, что до последнего / или @, и оставляем только буквы, цифры, подчеркивания
    pattern = r'(?:https?://)?(?:t\.me/|@)?([a-zA-Z0-9_]+)$'

    match = re.search(pattern, text.strip())
    if match:
        return match.group(1)
    return text.strip()  # если не нашли шаблон, возвращаем как есть
# get_smart_proccess_by_date()



def get_ceo_by_username_in_bitrix(username: str):
    url = 'https://rbbase.ru/rest/244/th59hcc5qids1hkp/crm.item.list'
    headers = {
        'Content-Type': 'application/json'
    }
    params = {
        'entityTypeId': 1088,  # ID вашего Smart-процесса
        'select': ['id', 'title', "ufCrm31_1758640107"],
        'filter': {
             '%ufCrm31_1758624931': username
        },
        # поля для выборки,

    }
    response = requests.post(url, headers={'Content-Type': 'application/json'}, data=json.dumps(params))
    if len(json.loads(response.content)['result']['items']) > 0:

        return json.loads(response.content)['result']['items'][0]['ufCrm31_1758640107']
    else:
        print(None)
        return None

