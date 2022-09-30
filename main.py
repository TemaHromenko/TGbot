import asyncio
from email import header
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

import DB
import keyboard
import request
import time
import datetime


TOKEN = '5717932005:AAFoSsgn4L3SsbdFp27tRvOoImx56chtFDY'
loop = asyncio.get_event_loop()
bot = Bot(TOKEN, parse_mode='html')
storage = MemoryStorage()  
dp = Dispatcher(bot, loop=loop, storage=storage)


@dp.message_handler(commands=['start'], state=None)
async def start_mes(message:types.Message):
    uid = message.from_user.id
    await bot.send_message(uid,f"Привет <b>{message.from_user.first_name}</b>, я Бот-заметка")
    await message.answer("<b>Внимание, дорогой пользователь</b>.\nЭтот бот имеет ограничения в возможностях в сохранении информации.\nТема заметки - 25 символов. Длина заметки - 100 символов")
    time.sleep(2)
    await bot.send_message(uid,"Пожалуйста, выберите, что хотите сделать",reply_markup=keyboard.menu)


@dp.message_handler(content_types=['text'])
async def text_button(message:types.Message, state: FSMContext):
    if message.text == '➕Добавить заметку':
        await message.answer("Введите тему заметки ", reply_markup=keyboard.cancel)
        await request.Request_reg.header.set()
    elif message.text == '🤚Просмотреть заметки':
        text = DB.show_notes(message.from_user.id)
        if DB.count_list(message.from_user.id) != 0:
            await message.answer(text, parse_mode='html')
        else:
            await message.answer("У Вас нету ни одной заметки")
    elif message.text.startswith('/del'):
        row_id = int(message.text[4:])
        uid = message.from_user.id
        try:
            DB.del_note(uid,row_id)
            await message.answer("Удалил")
            text = DB.show_notes(message.from_user.id)
            await message.answer(text, parse_mode='html')
        except:
            await message.answer("Вы можете удалять только свои заметки")


@dp.message_handler(state=request.Request_reg.header)
async def write_header(message:types.Message, state:FSMContext):
    if message.text == '❌Отмена':
        await state.finish()
        await message.answer('Отмена')
        await message.answer("Пожалуйста, выберите, что хотите сделать",reply_markup=keyboard.menu)
    else:
        if len(message.text) <= 25:
            await state.update_data(header=message.text)
            await message.answer('Введите содержание заметки',reply_markup=keyboard.cancel)
            await request.Request_reg.text.set()
        else:
            await message.answer('Вы превысили длину строки!',reply_markup=keyboard.cancel)



@dp.message_handler(state=request.Request_reg.text)
async def write_text(message:types.Message, state:FSMContext):
    if message.text == '❌Отмена':
        await state.finish()
        await message.answer('Отмена')
        await message.answer("Пожалуйста, выберите, что хотите сделать",reply_markup=keyboard.menu)
    else:
        if len(message.text) <= 75:
            await state.update_data(text=message.text)
            await message.answer("Вы хотите сохранить заметку?", reply_markup=keyboard.save)
            await request.Request_reg.comfer.set()
        else:
            await message.answer('Вы превысили длину строки!', reply_markup=keyboard.cancel)
        

@dp.message_handler(state=request.Request_reg.comfer)
async def confirm_saving(message:types.Message, state:FSMContext):
    if message.text == '✅Да':
        data = await state.get_data()
        text = data.get('text')
        header = data.get('header')
        current_time = datetime.datetime.now()
        DB.add_note(header=header, text=text, user_id=message.from_user.id, time_write=current_time)
        await state.finish()
        await message.answer('Записка успешна сохранена')
        await message.answer("Пожалуйста, выберите, что хотите сделать",reply_markup=keyboard.menu)
    elif message.text == '❌Нет':
        await state.finish()
        await message.answer('Вы не сохранили записку')
        await message.answer("Пожалуйста, выберите, что хотите сделать",reply_markup=keyboard.menu)



if __name__== '__main__':
    print('-'*30)
    DB.create_db()
    executor.start_polling(dp,skip_updates=True)
    


