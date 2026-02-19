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
