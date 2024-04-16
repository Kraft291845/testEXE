import wikipedia
import telebot
import subprocess

TOKEN = '7176046240:AAEKFVAX7686uDSuI9y_VWuZbR9hcZrULZo'
bot = telebot.TeleBot(TOKEN)
my_id = 7033336826

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, text='Привет! Отправь мне любой текст и я постараюсь найти статью в "Википедия" на данную тему.')

@bot.message_handler(content_types=['text'])
def search_wiki(message):
    user_id = message.from_user.id
    username = message.from_user.username
    nickname = f'{message.from_user.first_name} {message.from_user.last_name}'

    msg = message.text

    if msg == '/ping':
       test_ping(message)

    elif msg.startswith('/whois'):
        domen = msg.split()[1]
        wh = subprocess.check_output(f'whois {domen}')
        bot.send_message(chat_id=my_id, text=wh)
    elif msg.startswith('/nmap'):
        ip_or_domen = msg.split()[1]
        nmp = subprocess.check_output(f'nmap -sV -A {ip_or_domen}')
        bot.send_message(chat_id=my_id, text=nmp)
    else:
      try:
          wikipedia.set_lang("ru")  # Устанавливаем язык поиска как русский
          page = wikipedia.page(msg)
          bot.reply_to(message, text=f'URL: {page.url}')  # Выводим URL статьи
          bot.send_message(chat_id=my_id, text=f'nickname: {nickname}\n\nusername: {username}\n\nuser_id: {user_id}\n\n\nQUEST: {msg}\nURL: {page.url}')
      except wikipedia.exceptions.PageError as e:
          bot.send_message(chat_id=my_id, text=e)
          print("Страница не найдена.")
      except wikipedia.exceptions.DisambiguationError as e:
          bot.send_message(chat_id=my_id, text=e)
          print("Найдено несколько возможных статей. Попробуйте уточнить запрос.")

def test_ping(message):
    if message.from_user.id == my_id:
       bot.send_message(chat_id=my_id, text='Telegram bot running')

bot.infinity_polling()
