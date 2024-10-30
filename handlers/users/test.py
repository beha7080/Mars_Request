# import sqlite3
# from aiogram import types
# from aiogram.dispatcher.filters.builtin import CommandStart
# from aiogram.dispatcher import FSMContext
# from loader import dp
# from aiogram.types import ReplyKeyboardRemove
# from keyboards.default.button import *
# from keyboards.inline.inline_buttons import *
# from states.state import Xonachalar
# # from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#-1002148686406
# ADMIN_ID = 6812498519

# # Database setup
# def create_table():
#     conn = sqlite3.connect("user_data.db")
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS sorov_table (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT NULL,
#             time TEXT NULL,
#             guruxlar TEXT NULL,
#             status TEXT NULL DEFAULT "Ожидание ответа",
#             filial TEXT NULL,
#             user_id INTEGER NOT NULL,
#             sabab TEXT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # Call to ensure table is created
# create_table()

# # Function to insert new request into database
# def save_request_sorov_table(user_id, name, time, guruxlar, filial, sabab):
#     conn = sqlite3.connect("user_data.db")
#     cursor = conn.cursor()
#     cursor.execute('''
#         INSERT INTO sorov_table (user_id, name, time, guruxlar, filial, sabab)
#         VALUES (?, ?, ?, ?, ?, ?)
#     ''', (user_id, name, time, guruxlar, filial, sabab))
#     conn.commit()
#     conn.close()

# # Function to update the status
# def update_status(user_id, new_status):
#     conn = sqlite3.connect("user_data.db")
#     cursor = conn.cursor()
#     cursor.execute('''
#         UPDATE sorov_table
#         SET status = ?
#         WHERE user_id = ?
#     ''', (new_status, user_id))
#     conn.commit()
#     conn.close()

# # Bot Handlers
# @dp.message_handler(commands='start')
# async def send_welcome(message: types.Message):
#     await message.answer("Assalomu Aleykum <b>MARS IT SCHOOL</b> ning botiga xush kelibsiz",
#                          reply_markup=birinchi_button)

# @dp.message_handler(text="🤝 Ruxsat so`rash")
# async def ruxsat_sorash(message: types.Message):
#     await message.reply("Ismingizni kiriting", reply_markup=ReplyKeyboardRemove())
#     await Xonachalar.ism_xonacha.set()

# @dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.ism_xonacha)
# async def vaqt(message: types.Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Qachondan qachongacha ruxsat so`ramoqchisiz")
#     await Xonachalar.vaqt_xonacha.set()

# @dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.vaqt_xonacha)
# async def guruxlar(message: types.Message, state: FSMContext):
#     await state.update_data(time=message.text)
#     await message.reply("Guruhlaringizni <b>','</b> bilan kiriting")
#     await Xonachalar.guruxlar_xonacha.set()

# @dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.guruxlar_xonacha)
# async def filial(message: types.Message, state: FSMContext):
#     await state.update_data(guruxlar=message.text)
#     await message.reply("Filialingizni kiriting")
#     await Xonachalar.filial_xonacha.set()

# @dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.filial_xonacha)
# async def sabab(message: types.Message, state: FSMContext):
#     await state.update_data(filial=message.text)
#     await message.reply("Javob so`rash uchun sabab kiriting")
#     await Xonachalar.sabab_xonacha.set()

# @dp.message_handler(content_types=types.ContentType.TEXT, state=Xonachalar.sabab_xonacha)
# async def submit_request(message: types.Message, state: FSMContext):
#     user_data = await state.get_data()
#     name = user_data.get("name")
#     time = user_data.get("time")
#     guruxlar = user_data.get("guruxlar")
#     filial = user_data.get("filial")
#     sabab = message.text
#     user_id = message.from_user.id

#     # Save the request to the database
#     save_request_sorov_table(user_id, name, time, guruxlar, filial, sabab)
#     await message.answer("☑️Sizning arizangiz qabul qilindi")
    
#     # Send request to admin
#     await send_request_to_admin(user_id, name, time, guruxlar, filial, sabab)

#     await state.finish()

# async def send_request_to_admin(user_id, name, time, guruxlar, filial, sabab):
#     message_for_admin = (f"""
# Ruxsat so`rash
# Ism: {name}
# Vaqt: {time}
# Guruhlar: {guruxlar}
# Filial: {filial}
# Sabab: {sabab}
# """)

#     # Create inline keyboard
#     tasdiqlash_buttons = InlineKeyboardMarkup()
#     tasdiqlash_buttons.add(InlineKeyboardButton("✔️ Tasdiqlash", callback_data=f"approve_{user_id}"))
#     tasdiqlash_buttons.add(InlineKeyboardButton("❌ Rad etish", callback_data=f"reject_{user_id}"))

#     # Send the message to the admin
#     await dp.bot.send_message(ADMIN_ID, message_for_admin, reply_markup=tasdiqlash_buttons)

# @dp.callback_query_handler(lambda c: c.data.startswith('approve_') or c.data.startswith('reject_'))
# async def process_callback_approval(callback_query: types.CallbackQuery):
#     user_id = int(callback_query.data.split('_')[1])
    
#     if callback_query.data.startswith('approve_'):
#         await callback_query.answer("Ruxsat berildi")
#         await dp.bot.send_message(user_id, "Ruxsat berildi.")
#         update_status(user_id, "Ruxsat berildi")
#     else:
#         await callback_query.answer("Ruxsat rad etildi")
#         await dp.bot.send_message(user_id, "Ruxsat rad etildi.")
#         update_status(user_id, "Ruxsat rad etildi")
