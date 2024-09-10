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
                try:
                    geo_data = WeatherService.get_geo_data(city)
                except WeatherServiceException as wse:
                    self.send_message(str(wse))
                else:
                    buttons = []
                    for item in geo_data:
                        test_button = {
                            'text': f'{item.get("name")} - {item.get("country_code")}',
                            'callback_data': json.dumps(
                                {'type': 'weather', 'lat': item.get('latitude'), 'lon': item.get('longitude')})
                        }
                        buttons.append([test_button])
                    markup = {
                        'inline_keyboard': buttons
                    }
                    self.send_markup_massage('Choose a city from a list:', markup)


class CallbackHandler(TelegramHandler):

    def __init__(self, data):
        self.user = User(**data.get('from'))
        self.callback_data = json.loads(data.get('data'))

    def handle(self):
        callback_type = self.callback_data.pop('type')
        match callback_type:
            case 'weather':
                try:
                    weather = WeatherService.get_current_weather_by_geo_data(**self.callback_data)
                except WeatherServiceException as wse:
                    self.send_message((str(wse)))
                else:
                    self.send_message(json.dumps(weather))
