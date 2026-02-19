<<<<<<< HEAD
from aiogram import Bot, Dispatcher, executor, types
from django.contrib.messages.context_processors import messages

from config import token
from check import *

bot = Bot(token)
dp = Dispatcher(bot)

start_text = '''Здравствуй, я -  бот предназначенный для автоматической проверки теста'''
start_markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton('Начать' , callback_data='start')
start_markup.add(button1)

sensitivity = 100

def get_resultMessage(result):
    # Проверка в дальнейшем должна включать не конкретный тест, а введеный пользователем, с правильными ответами
    fin_message = "Вот твои результаты:\n"
    points = 0

    if result[0:3] == [1, 0 ,0]:
        fin_message += "1.Верно\n"
        points +=1
    else:
        fin_message += "1.Неверно\n"

    if result[3:7] == [1, 0, 0, 0]:
        fin_message += "2.Верно\n"
        points += 1
    else:
        fin_message += "2.Неверно\n"

    if result[7:11] == [0, 1, 0 ,0]:
        fin_message += "3.Верно\n"
        points += 1
    else:
        fin_message += "3.Неверно\n"

    if result[11:] == [0, 1]:
        fin_message += "4.Верно\n"
        points += 1
    else:
        fin_message += "4.Неверно\n"

    fin_message += f"\nТвои баллы: {points}"

    return fin_message

@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await bot.send_message(message.chat.id, start_text ,parse_mode='HTML', reply_markup=start_markup)

@dp.message_handler(commands=['parameters'])
async def prmtrs(message: types.Message):
    await bot.send_message(message.chat.id, text="Введите параметр порога чувствительности от 0 до 255\n(число, обозначающее средний цвет квадрата, по которому мы судим, есть ли метка в квадрате или нет)\nФормат ввода:\nЧувствительность: 125")

@dp.message_handler(content_types='photo')
async def resolve(message: types.Message):
    global sensitivity
    await message.photo[-1].download(destination_file='img.jpg')

    result = check('img.jpg', sensitivity)
    resultMessage = get_resultMessage(result)
    await bot.send_message(message.chat.id, text= resultMessage)

    with open('img.jpg' , 'rb') as photo:
        await message.answer_photo(photo)

@dp.message_handler()
async def get_prmts(message: types.Message):
    global sensitivity
    text = message.text.lower()
    num = -1

    try:
        num = int(message.text[-3:])
    except:
        await bot.send_message(message.chat.id, text="Неверный ввод параметра")

    if "чувствительность" in text and not(num >255 or num<0):
        sensitivity = num
        await bot.send_message(message.chat.id, text="Успешный ввод параметра")
    else:
        await bot.send_message(message.chat.id, text="Неверный ввод")

@dp.callback_query_handler()
async def callback(callback:types.CallbackQuery):
    if callback.data == 'start':
     await callback.bot.send_message(callback.message.chat.id,
                                '<em>Отправь мне фото решенного теста, в котором отчетливо видно текст</em>',
                                     parse_mode='HTML')
     await callback.answer('жду фоток')

executor.start_polling(dp)
=======
from aiogram import Bot, Dispatcher, executor, types
from config import token
from check import *

bot = Bot(token)
dp = Dispatcher(bot)

start_text = '''<em>Здравствуй, этот бот предназначен для автоматической проверки теста</em>'''
start_markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton('Начать' , callback_data='start')
start_markup.add(button1)

sensitivity = 100

@dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    await bot.send_message(message.chat.id, start_text ,parse_mode='HTML', reply_markup=start_markup)

@dp.message_handler(commands=['parameters'])
async def prmtrs(message: types.Message):
    await bot.send_message(message.chat.id, text="Введите параметр порога чувствительности от 0 до 255\n(число, обозначающее средний цвет квадрата, по которому мы судим, есть ли метка в квадрате или нет)\nФормат ввода:\nЧувствительность: 125")

@dp.message_handler(content_types='photo')
async def resolve(message: types.Message):
    global sensitivity
    await message.photo[-1].download(destination_file='img.jpg')

    result = check('img.jpg', sensitivity)

    await bot.send_message(message.chat.id,
                           text=f"Итоговый результат: {result}"
                           )

    with open('img.jpg' , 'rb') as photo:
        await message.answer(text=str(len(result)))
        await message.answer_photo(photo)

@dp.message_handler()
async def get_prmts(message: types.Message):
    global sensitivity
    text = message.text.lower()
    num = -1

    try:
        num = int(message.text[-3:])
    except:
        await bot.send_message(message.chat.id, text="Неверный ввод параметра")

    if "чувствительность" in text and not(num >255 or num<0):
        sensitivity = num
        await bot.send_message(message.chat.id, text="Успешный ввод параметра")
    else:
        await bot.send_message(message.chat.id, text="Неверный ввод")

@dp.callback_query_handler()
async def callback(callback:types.CallbackQuery):
    if callback.data == 'start':
     await callback.bot.send_message(callback.message.chat.id,
                                '<em>Отправь нам фото решенного теста, в котором отчетливо видно текст</em>',
                                     parse_mode='HTML')
     await callback.answer('жду фоток')

executor.start_polling(dp)
>>>>>>> 96de381de56a01310ca6c9bf61f24480f87ffddd
