import telebot
import logging
import time
from telebot import types

import data, api
# Замените 'YOUR_API_TOKEN' на свой токен API
API_TOKEN = ''

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

recipe = None


@bot.message_handler(commands=['recipes'])
def Recipe(message):
     global recipe
     #user_name = message.from_user.first_name
     #user_id = message.from_user.id
     name = message.text[8:]
     bot.send_message(message.chat.id, "Пожалуйста подождите")
     
     recipe = api.search_meal_by_name(name)
     
     markup = types.InlineKeyboardMarkup(row_width=1)
     
     item1 = types.InlineKeyboardButton(
        text='Сохранить', callback_data='save_recipe')
    
     markup.add(item1)
     print(recipe)
     bot.send_message(message.chat.id, recipe[0], reply_markup=markup)
     
                           
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    global recipe
    if call.data == "food_list":
    	
    	markup = types.InlineKeyboardMarkup(row_width=1)
    	
    	all_recipe = data.all_recipes(call.message.chat.id)
    	
    	for el in all_recipe:
    	    markup.add(types.InlineKeyboardButton(
        text=el[1], callback_data='recipe'))
    	
    	bot.send_message(call.message.chat.id, 'food list', reply_markup=markup)
    	
    elif call.data == "reffer":
    	
    	user_id = call.message.chat.id
    	
    	bot_name = bot.get_me()
    	
    	ref_url = f"Твоя реферальная ссылка:\nhttps://t.me/{bot_name.username}?start={user_id}\nКол-во твоих рефералов: {data.count_referals(user_id)}"
    	bot.send_message(call.message.chat.id, ref_url)
 
    elif call.data == "save_recipe":
    	print("сохранено")
    	data.save_recipe(recipe[0],recipe[1][16:], call.message.chat.id)
    	

if __name__ == "__main__":
    bot.polling(none_stop=True)