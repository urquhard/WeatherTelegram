import telebot
import requests
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

consts = {}
consts["TOKEN"] = "6269053129:AAFzB0jN29F1T9JALhhE1zeB-BIMY3E4nJI"
consts["API_KEY"] = "c30a08f2d4f2b5604579f1c379066879"
consts["URL_WEATHER_API"] = "https://api.openweathermap.org/data/2.5/weather"


EMOJI_CODE = {200: '⛈', 804: '⛈'}  # словарь с emoji

bot = telebot.TeleBot(consts["TOKEN"])

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)  # добавление клавиатуры
keyboard.add(KeyboardButton("Get weather", request_location=True))
keyboard.add(KeyboardButton("Author"))

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
        city_name = response['name']
        description = response['weather'][0]['desciption']
        code = response['weather'][0]["id"]
    except Exception as e:
        raise Exception(f"Failed to parse weather API: {e}")
    
    emoji = EMOJI_CODE.get(code, "NULL")
    message = f"Weather in {city_name}\n"
    message += f"{emoji} {description.capitalize()}\n"
    return message

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Приветственное сообщение."""
    response = "Send your geo to get weather"
    bot.send_message(message.chat.id, response, reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def send_weather(message):
    """Извлечение координат и отправка ответа."""
    lon, lat = message.location.longitude, message.location.latitude
    try:
        current_weather = get_weather(lon, lat)
        bot.send_message(message.chat.id, current_weather, reply_markup=keyboard)
    except Exception:
        bot.send_message(message.chat.id, "Weather in this region is unavailable", reply_markup=keyboard)

@bot.message_handler(regexp='О проекте')
def send_about(message):
    """Сообщение о проекте."""
    bot.send_message(message.chat.id, "Bot is made by genius gang", reply_markup=keyboard)

bot.infinity_polling()
