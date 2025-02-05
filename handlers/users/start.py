import sqlite3
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.default.button import birinchi_button
from states.state import Xonachalar
from database_saver import save_request_sorov_table, update_status, save_request_to_history, get_user_data

ADMIN_ID = "YOUR_ADMIN_ID"
GROUP_ID = "YOUR_GROUP"


#salom

# Bot Handlers
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await message.answer("Assalomu Aleykum <b>MARS IT SCHOOL</b> ning botiga xush kelibsiz",
                         reply_markup=birinchi_button)

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

    # Ma'lumotlarni bazaga saqlash
    save_request_sorov_table(user_id, name, time, guruxlar, filial, sabab)
    await message.answer("☑️ Sizning arizangiz qabul qilindi")

    # Ruxsat so'rovini adminlarga yuborish
    await send_request_to_admin(user_id, name, time, guruxlar, filial, sabab)

    await state.finish()

async def send_request_to_admin(user_id, name, time, guruxlar, filial, sabab):
    message_for_admin = (f"""
Ruxsat so`rash boyicha!
🆔 Telegram ID: {user_id}
👤 Ism: {name}
⏳ Vaqt: {time} 
👥 Guruhlar: {guruxlar}
📍 Filial: {filial}
❓ Sabab: {sabab}
""")

    # Inline tugmalarni yaratish
    tasdiqlash_buttons = InlineKeyboardMarkup()
    tasdiqlash_buttons.add(InlineKeyboardButton("✔️ Tasdiqlash", callback_data=f"approve_{user_id}"))
    tasdiqlash_buttons.add(InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user_id}"))

    # Xabarni adminlarga yuborish
    await dp.bot.send_message(ADMIN_ID, message_for_admin, reply_markup=tasdiqlash_buttons)

@dp.callback_query_handler(lambda c: c.data.startswith('approve_') or c.data.startswith('reject_'))
async def process_callback_approval(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split('_')[1])
    status_text = ""
    

    if callback_query.data.startswith('approve_'):
        status_text = "Ruxsat berildi"

        # Foydalanuvchi ma'lumotlarini bazadan olish
        user_data = get_user_data(user_id)  # Bazadan foydalanuvchi ma'lumotlarini olish
        if user_data:
            message_for_group = f"""
<b>{status_text}</b>
Ruxsat so'rov holati:
🆔 Telegram ID: {user_id}
👤 Ism: {user_data['name']}
⏳ Vaqt: {user_data['time']}
👥 Guruhlar: {user_data['guruxlar']}
📍 Filial: {user_data['filial']}
❓ Sabab: {user_data['sabab']}
"""
            await bot.send_message(GROUP_ID, message_for_group, parse_mode="HTML")
    else:
        status_text = "Ruxsat rad etildi"

    # Foydalanuvchiga javob yuborish
    await callback_query.answer(status_text)
    await dp.bot.send_message(user_id, status_text)

    # Holatni sorov_table da yangilash
    update_status(user_id, status_text)

    # Ariza ma'lumotlarini history_sorov ga ko'chirish va sorov_table dan o'chirish
    save_request_to_history(user_id)
