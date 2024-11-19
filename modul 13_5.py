from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio



api = ' '
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_r = types.KeyboardButton(text='Рассчитать')
button_i = types.KeyboardButton(text='Информация')
kb.add(button_r, button_i)



@dp.message_handler(commands=['start'])
async def consol_command(messeage):
    await messeage.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup = kb)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()


@dp.message_handler(text='Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight=message.text)
    await message.answer('Введите свой пол "м" или "ж"')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender=message.text.lower())
    data = await state.get_data()
    if str(data['gender']) == 'м':
        calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
        await message.answer(f'Ваши калории {calories}')
    elif data['gender'] == 'ж':
        calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age'])-161
        await message.answer(f'Ваши калории {calories}')
    else:
        await message.answer(f'невозможно высчитать, пол введен не по образцу')
    await state.finish()


@dp.message_handler()
async def other_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)