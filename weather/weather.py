import requests
from settings import settings
#TO DO: MAKE ALL KEYS PRIVATE

consts = {} 

consts["TOKEN"] = settings.telegram_token
consts["API_KEY"] = settings.open_weather_api
consts["URL_WEATHER_API"] = settings.url_weather_api


EMOJI_CODE = {200: '⛈', 804: '⛈'}  # словарь с emoji


def get_weather(lat, lon):
    """Запрос к API и возврат строки с ответом."""
    params = {"appid": consts["API_KEY"],
              "lat": lat,
              "lon": lon,
              "lang": "en",
              "units": "metric",
              }
    try:
        response = requests.get(consts["URL_WEATHER_API"], params=params).json()
        print(response)
        city_name = response['name']
        description = response['weather'][0]['description']
        code = response['weather'][0]["id"]
    except Exception as e:
        raise Exception(f"Failed to parse weather API: {e}")
    
    emoji = EMOJI_CODE.get(code, "NULL")
    message = f"Weather in {city_name}\n"
    message += f"{emoji} {description.capitalize()}\n"
    return message
