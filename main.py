import aioschedule
from aiogram import Bot, filters, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.client.session.aiohttp import AiohttpSession
from config import TOKEN
import asyncio
import jsonwriter
import time

# session = AiohttpSession(proxy="http://proxy.server:3128")
bot = Bot(token=TOKEN)
dp = Dispatcher()

schedule_actions_inline = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Текущие занятия🗒", callback_data="check_trains")],
                                                                      [types.InlineKeyboardButton(text="Добавить/удалить занятие📌", callback_data="add_train")],
                                                                      [types.InlineKeyboardButton(text="Уведомления о тренировках🔊", url="https://t.me/sport_noti_bot?command=start")]])

mon = types.KeyboardButton(text="Понедельник1️⃣")
tue = types.KeyboardButton(text="Вторник️2️⃣")
wed = types.KeyboardButton(text="Среда3️⃣")
thu = types.KeyboardButton(text="Четверг4️⃣")
fri = types.KeyboardButton(text="Пятница5️⃣")
sat = types.KeyboardButton(text="Суббота6️⃣")
sun = types.KeyboardButton(text="Воскресенье7️⃣")
days_keyboard = types.ReplyKeyboardMarkup(keyboard=[
    [mon, tue, wed],
    [thu, fri, sat],
    [sun]
], resize_keyboard=True)
back_main_inline = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Назад", callback_data="add_train")],[types.InlineKeyboardButton(text="На главную", callback_data="schedule")]])
main_inline = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="На главную", callback_data="schedule")]])
add_del_inline = types.InlineKeyboardMarkup(inline_keyboard=[[types.InlineKeyboardButton(text="Добавить", callback_data="add")],[types.InlineKeyboardButton(text="Удалить", callback_data="del")]])

@dp.message(Command("start"))
async def start_reply(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}")
    await message.answer("Выбери действие", reply_markup=schedule_actions_inline)
    jsonwriter.write_user("schedules.json", message.from_user.id)
@dp.callback_query(F.data == "schedule")
async def schedule(callback: types.CallbackQuery):
    await callback.message.edit_text("Выбери действие", reply_markup=schedule_actions_inline)
@dp.callback_query(F.data == "add_train")
async def add_train(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Выберите день", reply_markup=days_keyboard)
@dp.callback_query(F.data == "check_trains")
async def see_trains(callback: types.CallbackQuery):
    await callback.message.edit_text(jsonwriter.return_trains("schedules.json", callback.from_user.id))
    await callback.message.answer("Не забывай)", reply_markup=main_inline)
@dp.callback_query(F.data == "add")
async def add(callback: types.CallbackQuery):
    userID = callback.from_user.id
    process_data = jsonwriter.read_json("process.json")
    day = process_data[str(userID)]["day"]
    time = process_data[str(userID)]["time"]
    jsonwriter.add_write_time("schedules.json", userID, day, time)
    jsonwriter.del_process("process.json", userID)
    await callback.message.edit_text("Занятие успешно добавлено", reply_markup=main_inline)
@dp.callback_query(F.data == "del")
async def delete_training(callback: types.CallbackQuery):
    try:
        userID = callback.from_user.id
        process_data = jsonwriter.read_json("process.json")
        day = process_data[str(userID)]["day"]
        time = process_data[str(userID)]["time"]
        jsonwriter.delete_train("schedules.json", userID, time, day)
        jsonwriter.del_process("process.json", userID)
        await callback.message.edit_text("Занятие успешно удалено", reply_markup=main_inline)
    except:
        await callback.message.edit_text("Такого занятия нет", reply_markup=main_inline)
@dp.message()
async def day_write(message: types.Message):
    if(len(message.text) >= 6 and message.text[0].isalpha()):
        day = message.text[0:-3]
        await message.answer("Введите время", reply_markup=back_main_inline)
        jsonwriter.write_train("process.json", message.from_user.id, day)
    elif(len(message.text) == 5 and message.text[0].isdigit()):
        try:
            var = time.strptime(message.text, '%H:%M')
            train_time = message.text
            jsonwriter.process_time("process.json", message.from_user.id, train_time)
            await message.answer("Выберите действие", reply_markup=add_del_inline)
        except:
            await message.answer("Введите правильное время")
    else:
        await message.answer("Введите правильный день или время")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())