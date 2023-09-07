import telebot
import logging
import time
from telebot import types

import data
# Замените 'YOUR_API_TOKEN' на свой токен API
API_TOKEN = '5446068256:AAE47yTitsLjZbHxLnLAFf-rITPaeElqOgg'

# Инициализация бота
bot = telebot.TeleBot(API_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    welcome_message = f"Привет, {user_name}!"
    
    ref_id = message.text[7:]
    
    data.save_user(message.from_user.id, message.from_user.username, ref_id)
    
    logging.info(f'{message.from_user.id} {message.from_user.username} {time.asctime()}''/start')
    
    bot.send_message(message.chat.id, welcome_message)
    
@bot.message_handler(func=lambda message: message.text == "/profile")
def Profile(message):
     user_name = message.from_user.first_name
     user_id = message.from_user.id
     
     
     #кнопки
     markup = types.InlineKeyboardMarkup(row_width=1)
     
     item1 = types.InlineKeyboardButton(
        text='Список Блюд', callback_data='food_list')
     item2 = types.InlineKeyboardButton(
        text='Рефералка', callback_data='reffer')
    
     markup.add(item1, item2)
     
     bot.send_message(message.chat.id,f"{user_name}\nID:{user_id}", reply_markup=markup)
 
         
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == "food_list":
    	bot.send_message(call.message.chat.id, 'food list')
    	
    elif call.data == "reffer":
    	
    	user_id = call.message.chat.id
    	
    	bot_name = bot.get_me()
    	
    	
    	
    	ref_url = f"Твоя реферальная ссылка:\nhttps://t.me/{bot_name.username}?start={user_id}\nКол-во твоих рефералов: {data.count_referals(user_id)}"
    	bot.send_message(call.message.chat.id, ref_url)

if __name__ == "__main__":
    bot.polling(none_stop=True)