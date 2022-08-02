import logging
from datetime import datetime
import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from bot.config import TOKEN_WEATHER
from bot.loader import dp
from bot.models.model_chat import respond_to_dialog
from bot.models.model_compose import tokenizer, model
from bot.states.states import Test


@dp.message_handler(commands='start')
async def start(message: types.message):
    start_button = ['погода', 'стихи', 'болталка', 'отмена']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_button)

    await message.answer('Привет, что тебе нужно?', reply_markup=keyboard)

@dp.message_handler(Text(equals=['отмена','cancel','stop','стоп']), state='*')
@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    await state.finish()
    await message.reply('Cancelled.')

@dp.message_handler(Text(equals=['weather', 'погода', 'какая погода']))
@dp.message_handler(commands='weather')
async def q_weather(message: types.message):
    await message.answer('В каком городе посмотреть погоду?')
    await Test.weather.set()

@dp.message_handler(state=Test.weather)
async def get_weather(message: types.message):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={TOKEN_WEATHER}&units=metric")
        data = r.json()
        city = data["name"]
        temp = data["main"]["temp"]
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
                            f"Температура в городе {city} составляет: {temp}C°"
                            )
    except:
        await message.answer('Я такого города не знаю. Извини')

@dp.message_handler(Text(equals=['chat', 'болталка', 'давай поболтаем', 'поговорим?']))
@dp.message_handler(commands='chat')
async def q_chat(message: types.message):
    await message.answer('О чем поговорим?')
    await Test.chat.set()

@dp.message_handler(state=Test.chat)
async def chat(message: types.message):
    seed = message.text
    history = [seed]
    result = respond_to_dialog(history[-10:])
    next_sentence = result
    await message.answer(f'{next_sentence}')

@dp.message_handler(Text(equals=['compose', 'стихи', 'напиши стихи']))
@dp.message_handler(commands='compose')
async def q_compose(message: types.Message):
    await message.answer('Начни, а я продолжу..')
    await Test.compose.set()

@dp.message_handler(state=Test.compose)
async def poetry(message: types.Message):
    await message.answer('Please stand by...')
    prefix = message.text
    tokens = tokenizer(prefix, return_tensors='pt')
    size = tokens['input_ids'].shape[1]
    output = model.generate(
        **tokens,
        do_sample=False,
        max_length=size+500,
        repetition_penalty=5.,
        temperature=0.8,
        num_beams=10,
    )
    decoded = tokenizer.decode(output[0])
    result = decoded[len(prefix):]
    await message.answer(prefix + result)
