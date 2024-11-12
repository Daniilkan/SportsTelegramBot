import asyncio
import time

from aiogram import Bot, filters, Dispatcher, types, F
from aiogram.client.session.aiohttp import AiohttpSession
from config import NOTI_TOKEN

bot = Bot(token=NOTI_TOKEN)
dp = Dispatcher()

import datetime
import pytz
import jsonwriter
import parser

weekdays = {
    "Понедельник": 1,
    "Вторник": 2,
    "Среда": 3,
    "Четверг": 4,
    "Пятница": 5,
    "Суббота": 6,
    "Воскресенье": 7
}
on_markup = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Включить уведомления🔊", callback_data="on")]])

@dp.message()
async def notifies(message: types.Message):
    if(message.text == "/start"):
        await message.answer("Этот бот служит напоминалкой о тренировках @sports_help_bot", reply_markup=on_markup)

@dp.callback_query(F.data == "on")
async def turn_on(callback: types.CallbackQuery):
    await callback.message.edit_text("Теперь тебе будут приходить уведомления о тренировках")
    while 1:
        today = datetime.date.today()
        day = today.isoweekday()
        currenthour = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).hour)
        currentmin = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).minute)
        currentsec = int(datetime.datetime.now(pytz.timezone('Europe/Moscow')).second)
        data = jsonwriter.read_json("schedules.json")
        for i in data[str(callback.from_user.id)]["Trains"]:
            if weekdays[i] == day:
                for j in data[str(callback.from_user.id)]["Trains"][i]:
                    if int(j[0:2]) - currenthour == 1 and currentmin - int(j[3:5]) == 0 and currentsec == 1:
                        await callback.message.answer("Не забудь про тренировку в " + j)
                        await asyncio.sleep(1)
        if currenthour == 15 and currentmin == 53 and currentsec == 1:
            await callback.message.answer("Совет дня: " + parser.get_adivice())
            await callback.message.answer("Для поддержки обмена веществ желательно выпить стакан воды сейчас.")
            await asyncio.sleep(1)
        elif currenthour == 8 and currentmin == 0 and currentsec == 1:
            await callback.message.answer("Не забудьте про стакан воды с утра!")
            await asyncio.sleep(1)
        elif currenthour == 20 and currentmin == 0 and currentsec == 1:
            await callback.message.answer("Еще один стакан воды не помешал бы.")
            await asyncio.sleep(1)
        await asyncio.sleep(0.5)

async def main():
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())