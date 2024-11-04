import telebot
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

facts_ru = [
    "Самый крупный снежный человек был найден в Гималаях.",
    "Человек может прожить без воды всего несколько дней.",
    "Самая высокая гора в мире — Эверест.",
    "Самая глубокая точка океана — Марианская впадина.",
    "Скорость света составляет 299792458 метров в секунду.",
    "Самая длинная река в мире — Нил.",
    "Самое большое животное на Земле — синий кит.",
    "Человек может различать до 10 миллионов цветов.",
    "Самая древняя известная цивилизация — шумеры.",
    "Самая маленькая птица в мире — колибри."
]

facts_tt = [
    "Иң зур кар кешесе Һималайда табылган.",
    "Кеше сусыз берничә көн генә яши ала.",
    "Дөньядагы иң биек тау — Эверест.",
    "Океанның иң тирән ноктасы — Мариан чокыры.",
    "Яктылык тизлеге 299792458 метр/секунд.",
    "Дөньядагы иң озын елга — Нил.",
    "Җирдәге иң зур хайван — зәңгәр кит.",
    "Кеше 10 миллионга кадәр төс аера ала.",
    "Иң борынгы мәгълүм цивилизация — шумерлар.",
    "Дөньядагы иң кечкенә кош — колибри."
]

user_lang = {}
user_last_fact = {}

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Татарча", callback_data="lang_tt"))
    markup.add(InlineKeyboardButton("Русский", callback_data="lang_ru"))
    bot.send_message(message.chat.id, "Сәлам! Телне сайлагыз:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def callback_query(call):
    if call.data == "lang_ru":
        user_lang[call.from_user.id] = 'ru'
        lang_text = "Вы выбрали Русский язык."
        button_text = "Запросить факт"
    elif call.data == "lang_tt":
        user_lang[call.from_user.id] = 'tt'
        lang_text = "Сез Татар телен сайладыгыз."
        button_text = "Факт сорау"

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(button_text, callback_data="get_fact"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=lang_text, reply_markup=markup)
    user_last_fact[call.from_user.id] = None

@bot.callback_query_handler(func=lambda call: call.data == "get_fact")
def send_fact(call):
    lang = user_lang.get(call.from_user.id, 'tt')
    last_fact = user_last_fact.get(call.from_user.id)
    
    if lang == 'ru':
        fact_list = facts_ru
        button_text = "Запросить факт"
    else:
        fact_list = facts_tt
        button_text = "Факт сорау"

    fact = random.choice(fact_list)
    while fact == last_fact:
        fact = random.choice(fact_list)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(button_text, callback_data="get_fact"))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
    bot.send_message(call.message.chat.id, fact, reply_markup=markup)

    user_last_fact[call.from_user.id] = fact

bot.polling()
