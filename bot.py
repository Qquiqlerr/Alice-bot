import requests
from bs4 import BeautifulSoup
from telebot.async_telebot import AsyncTeleBot
import openai
from telebot import types
import random
import os
import json
import io
import asyncio
#var
PROMPT = 'Cute kitten in the house'

def startupCheckTelegramApi():
    if os.path.isfile('key_tg_api.json') and os.access('key_tg_api.json', os.R_OK):
        # checks if file exists
        print ("Telegram api key is ok")
        with open("key_tg_api.json", "r") as read_file:
            key = json.load(read_file)
            return key
    else:
        print("Enter a Telegram api key:")
        key_ = input()
        with io.open(os.path.join('', 'key_tg_api.json'), 'w') as db_file:
            db_file.write(json.dumps(key_))

def startupCheckOpenaiApi():
    if os.path.isfile('key_openai.json') and os.access('key_openai.json', os.R_OK):
        # checks if file exists
        print ("Openai api key exists and is readable, starting the program..")
        with open('key_openai.json', "r") as read_file:
            key = json.load(read_file)
            return key
    else:
        print("Enter a Openai api key:")
        key_ = input()
        with io.open(os.path.join('', 'key_openai.json'), 'w') as db_file:
            db_file.write(json.dumps(key_))

def sendhoroscope():
    url = ("https://horoscopes.rambler.ru/capricorn")
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup.find("div", class_="_1E4Zo _3BLIa").text

#API
bot = AsyncTeleBot(startupCheckTelegramApi())
openai.api_key = startupCheckOpenaiApi()

#Buttons
send_comp = types.KeyboardButton('Получить комплимент')
send_cat = types.KeyboardButton('Получить котика')
send_NeuroCat = types.KeyboardButton('Получить нейрокотика')
send_horo = types.KeyboardButton('Получить гороскоп на сегодня')
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(send_cat)
markup.add(send_comp)
markup.add(send_NeuroCat)
markup.add(send_horo)
#path
path = ['Cats/1628760997_16-p-foto-kotyat-milikh-i-nyashnikh-17.jpg',
        'Cats/1628904992_46-p-skachat-foto-milikh-kotikov-50.jpg',
        'Cats/1628905045_202-p-skachat-foto-milikh-kotikov-216.jpg',
        'Cats/1642798609_64-damion-club-p-malenkii-milii-kotenok-65.jpg',
        'Cats/1644933292_57-kartinkin-net-p-kartinki-milikh-kotikov-64.jpg',
        'Cats/1661756359_j-39.jpg',
        'Cats/kotenok-koshka-kot.jpg']




@bot.message_handler(commands=["start"])
async def return_text_digit(msg):
    await bot.send_message(msg.chat.id, 'Что ты хочешь?)', reply_markup=markup)


@bot.message_handler(content_types=["text"])
async def return_text_digit(msg):
    if(msg.text == 'Получить комплимент'):
        completion = openai.Completion.create(model="text-davinci-003", prompt="Напиши длинный комплимент для Алисы", temperature=0.7,
                                              max_tokens=1000)
        await bot.send_message(msg.chat.id, completion.choices [0].text)
    elif(msg.text == 'Получить котика'):
        photo = open(path[random.randrange(7)],'rb')
        await bot.send_photo(msg.chat.id,photo)
        photo.close()
    elif msg.text == 'Получить нейрокотика':
        response = openai.Image.create(
            prompt=PROMPT,
            n=1,
            size="256x256",
        )
        await bot.send_photo(msg.chat.id, response["data"][0]["url"])
    elif msg.text == 'Получить гороскоп на сегодня':
        await bot.send_message(msg.chat.id, f'Алиса, вот твой гороскоп на сегодня❤️💕\n'
                                            f'{sendhoroscope()}')





asyncio.run(bot.infinity_polling())
