from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp, bot
from keyboards.default.button import *
from keyboards.inline.inline_buttons import tasdiqlash_buttons
from states.state import Xonachalar
from database_saver import save_request_sorov_table, update_status, save_request_to_history, get_user_data

ADMIN_ID = 1091591701
GROUP_ID = -4270625456

@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.answer("Assalomu Aleykum <b>MARS IT SCHOOL</b> ning botiga xush kelibsiz", reply_markup=birinchi_button)

@dp.message_handler(text="🤝 Ruxsat so`rash")
async def ruxsat_sorash(message: types.Message):
    await message.reply("Ismingizni kiriting", reply_markup=ReplyKeyboardRemove())
    await Xonachalar.ism_xonacha.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.ism_xonacha)
async def vaqt(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Qachondan qachongacha ruxsat so`ramoqchisiz")
    await Xonachalar.vaqt_xonacha.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.vaqt_xonacha)
async def guruxlar(message: types.Message, state: FSMContext):
    await state.update_data(time=message.text)
    await message.reply("Guruhlaringizni <b>','</b> bilan kiriting")
    await Xonachalar.guruxlar_xonacha.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.guruxlar_xonacha)
async def filial(message: types.Message, state: FSMContext):
    await state.update_data(guruxlar=message.text)
    await message.reply("Filialingizni kiriting")
    await Xonachalar.filial_xonacha.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.filial_xonacha)
async def sabab(message: types.Message, state: FSMContext):
    await state.update_data(filial=message.text)
    await message.reply("Javob so`rash uchun sabab kiriting")
    await Xonachalar.sabab_xonacha.set()

@dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.sabab_xonacha)
async def submit_request(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    name = user_data.get("name")
    time = user_data.get("time")
    guruxlar = user_data.get("guruxlar")
    filial = user_data.get("filial")
    sabab = message.text
    user_id = message.from_user.id

    save_request_sorov_table(user_id, name, time, guruxlar, filial, sabab)
    await message.answer("☑️Sizning arizangiz qabul qilindi")
    await send_request_to_admin(user_id, name, time, guruxlar, filial, sabab)
    await state.finish()

async def send_request_to_admin(user_id, name, time, guruxlar, filial, sabab):
    message_for_admin = f"""
Ruxsat so`rash bo'yicha!
Telegram ID: {user_id}
Ism: {name}
Vaqt: {time}
Guruhlar: {guruxlar}
Filial: {filial}
Sabab: {sabab}
"""
    await bot.send_message(ADMIN_ID, message_for_admin, reply_markup=tasdiqlash_buttons)

@dp.callback_query_handler(text="tasdiqlash")
async def approve_request(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await handle_approval(callback_query, user_id, approved=True)

@dp.callback_query_handler(text="rad_etish")
async def reject_request(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await handle_approval(callback_query, user_id, approved=False)

async def handle_approval(callback_query: types.CallbackQuery, user_id: int, approved: bool):
    user_data = get_user_data(user_id)

    if approved:
        status_text = "TASDIQLANGAN"
        await callback_query.answer("Ruxsat berildi")
        await bot.send_message(user_id, "Ruxsat berildi.")
        update_status(user_id, "Ruxsat berildi")
    else:
        status_text = "RAD ETILGAN"
        await callback_query.answer("Ruxsat rad etildi")
        await bot.send_message(user_id, "Ruxsat rad etildi.")
        update_status(user_id, "Ruxsat rad etildi")

    save_request_to_history(user_id)

    message_for_group = f"""
<b>{status_text}</b>
Ruxsat so'rov holati:
Telegram ID: {user_id}
Ism: {user_data['name']}
Vaqt: {user_data['time']}
Guruhlar: {user_data['guruxlar']}
Filial: {user_data['filial']}
Sabab: {user_data['sabab']}
"""
    await bot.send_message(GROUP_ID, message_for_group, parse_mode="HTML")
