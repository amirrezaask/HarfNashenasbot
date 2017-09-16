import telebot
import time
import pymongo
from django.utils.crypto import get_random_string
bot = telebot.TeleBot('420984603:AAGTqks4sskFa7jcBp2pYfKSQBJR3wmlj4Q')
mongo=pymongo.MongoClient()
database=mongo.harfbot
def extract_unique_code(text):
    return text.split()[1] if len(text.split()) > 1 else None
@bot.message_handler(regexp='^[^/].*')
def sender(message):
    print('@sender')
    print(">>>"+unique_code)
    target=database.users.find_one({"code":unique_code})
    bot.send_message(target['chat_id'],message.text)
@bot.message_handler(commands=['start'])
def start(message):
    print ("@start")
    global unique_code
    unique_code = extract_unique_code(message.text)
    target_code=unique_code
    #print(message)
    is_target_in=database.users.find_one({"code":unique_code})
    is_source_in=database.users.find_one({"username":message.from_user.username})
    if is_target_in is None:
        if unique_code=="":
            print("")
            #bot.send_message(message.chat.id,'your target is not in database')
        else:
            bot.send_message(message.chat.id,'your target is not in database')
    else:
        print(is_target_in['username'])
        bot.send_message(message.chat.id,is_target_in['username'])
    if is_source_in is None :
        database.users.insert_one({'code':get_random_string(48),"username":message.from_user.username,"chat_id":message.chat.id})
bot.polling()
