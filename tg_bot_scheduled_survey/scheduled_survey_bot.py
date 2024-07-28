# импорт библиотек
import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler


# устанавливаем токен
bot = telebot.TeleBot('TOKEN')

# создаем планировщик задач
scheduler = BackgroundScheduler()
scheduler.start()

# Глобальная переменная для хранения chat_id группы
chat_id = None

# Функция для отправки опроса
def send_poll():
    if chat_id:
        bot.send_poll(chat_id, "Кататься идем?", ["Да", "Нет"])

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_polling(message):
    global chat_id
    if message.chat.type in ["group", "supergroup"]:
        chat_id = message.chat.id
        bot.send_message(chat_id, "Опросы будут отправляться каждые 2 минуты.")
        scheduler.add_job(send_poll, 'interval', minutes=2, id='poll_job', replace_existing=True)

# Обработчик команды /stop
@bot.message_handler(commands=['stop'])
def stop_polling(message):
    global chat_id
    if message.chat.type in ["group", "supergroup"]:
        bot.send_message(message.chat.id, "Опросы остановлены.")
        scheduler.remove_job('poll_job')
        chat_id = None

# Запуск бота
bot.polling(none_stop=True, interval=0)
