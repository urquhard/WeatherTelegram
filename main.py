import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup

from weather import weather


bot = telebot.TeleBot(weather.consts["TOKEN"])

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)  # добавление клавиатуры
keyboard.add(KeyboardButton("Get weather", request_location=True))
keyboard.add(KeyboardButton("Author"))


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
        current_weather = weather.get_weather(lon, lat)
        bot.send_message(message.chat.id, current_weather, reply_markup=keyboard)
    except Exception:
        bot.send_message(message.chat.id, "Weather in this region is unavailable", reply_markup=keyboard)


@bot.message_handler(func=lambda s: s.text == "Author")
def send_about(message):
    """Сообщение о проекте."""
    bot.send_message(message.chat.id, "Bot is made by genius gang", reply_markup=keyboard)

bot.infinity_polling()
