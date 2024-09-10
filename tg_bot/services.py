import requests


class WeatherServiceException(Exception):
    pass


class NoInfoException(Exception):
    pass


class WeatherService:
    GEO_URL = 'https://geocoding-api.open-meteo.com/v1/search'
    WEATHER_URL = 'https://api.open-meteo.com/v1/forecast'
    SUN_URL = ''

    @staticmethod
    def get_geo_data(city_name):
        pass
        params = {
            'name': city_name
        }
        res = requests.get(f'{WeatherService.GEO_URL}', params=params)
        if res.status_code != 200:
            raise WeatherServiceException('Cannot get geo data')
        elif not res.json().get('results'):
            raise WeatherServiceException('City not found')
        return res.json().get('results')

    @staticmethod
    def get_current_weather_by_geo_data(lat, lon):
        pass
        params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': True
        }

        res = requests.get(f'{WeatherService.WEATHER_URL}', params=params)
        if res.status_code != 200:
            raise WeatherServiceException('Cannot get geo data')
        return res.json().get('current_weather')
    #
    # @staticmethod
    # def get_sun_data(lat, lon):
    #     url = f"https://api.sunrise-sunset.org/json?lat={lat}&lon={lon}"
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         sun_data = response.json()
    #         return sun_data
    #     else:
    #         raise Exception("Failed to fetch sun data")
