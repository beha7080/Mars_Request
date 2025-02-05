from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

tasdiqlash_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="✔️ Tasdiqlash", callback_data="tasdiqlash"),
            InlineKeyboardButton(text="✖️ Rad etish", callback_data="rad_etish")
        ]
    ], resize_keyboard=True
)



filial_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Yunusobod",callback_data="yunusobod_call"),
            InlineKeyboardButton(text="Tinchlik",callback_data="tinchlik_call"),
            InlineKeyboardButton(text="Chilonzor",callback_data="chilonzor_call"),
            InlineKeyboardButton(text="Sergeli",callback_data="sergeli_call"),
            InlineKeyboardButton(text="Maksim Gorki",callback_data="maksim_gorki_call"),
            InlineKeyboardButton(text="Oybek",callback_data="oybek_call"),
            InlineKeyboardButton(text="Minor",callback_data="minor_call"),
        ]
    ]
)