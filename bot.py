import datetime
import requests
from bs4 import BeautifulSoup
from telebot.async_telebot import AsyncTeleBot
import openai
from telebot import types
import random
import asyncio
import os
import json
import io

#var
PROMPT = 'cute cat in the forest'
timehoro1 = datetime.time(8,30)

def startupCheck():
    if os.path.isfile('key.json') and os.access('key.json', os.R_OK):
        # checks if file exists
        print ("Key exists and is readable, starting the program..")
        with open("key.json", "r") as read_file:
            key = json.load(read_file)
            return key
    else:
        print("Enter a key:")
        key_ = input()
        with io.open(os.path.join('', 'key.json'), 'w') as db_file:
            db_file.write(json.dumps(key_))


#API
bot = AsyncTeleBot(startupCheck())
openai.api_key = "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"

#Buttons
send_comp = types.KeyboardButton('Получить комплимент')
send_cat = types.KeyboardButton('Получить котика')
send_NeuroCat = types.KeyboardButton('Получить нейрокотика')
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(send_cat)
markup.add(send_comp)
markup.add(send_NeuroCat)
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
    while True:
        url = ("https://horoscopes.rambler.ru/capricorn")
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        await asyncio.sleep(60)
        date_time_current = datetime.datetime.now()
        time_now = date_time_current.time()
        if time_now.hour == timehoro1.hour and time_now.minute == timehoro1.minute:
            await bot.send_message(msg.chat.id,soup.find("div", class_="_1E4Zo _3BLIa").text)




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
    else:
        response = openai.Image.create(
            prompt=PROMPT,
            n=1,
            size="256x256",
        )
        await bot.send_photo(msg.chat.id,response["data"][0]["url"])


asyncio.run(bot.infinity_polling())
