import json

import requests
from .services import WeatherService, WeatherServiceException

BOT_TOKEN = '7542728298:AAHS9xQQfEQJqu8z5FWqYJHSsYJ2FewQtxk'
TG_BASE_URL = 'https://api.telegram.org/bot'


class User:
    def __init__(self, id, is_bot, first_name, last_name, username, language_code):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        # self.username = username
        self.language_code = language_code


class TelegramHandler:
    user = None

    def send_markup_massage(self, text, markup):
        data = {
            'chat_id': self.user.id,
            'text': text,
            'reply_markup': markup
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)

    def send_message(self, text):
        data = {
            'chat_id': self.user.id,
            'text': text
        }
        requests.post(f'{TG_BASE_URL}{BOT_TOKEN}/sendMessage', json=data)


class MassageHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.text = data.get('text')

    def handle(self):
        match self.text.split():
            case 'weather', city:
                geo_data = WeatherService.get_geo_data(city)
                test_button = {
                    'text': 'I am a test button',
                    'callback_data': json.dumps({'test': 'data'})
                }
                markup = {
                    'inline_keyboard': [[test_button]]
                }
                self.send_markup_massage('Test massage', markup)


class CallbackHandler(TelegramHandler):
    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.callback_data = json.loads(data.get('data'))

    def handle(self):
        self.send_message(f'Received date: {self.callback_data}')
