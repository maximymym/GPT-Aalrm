from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def script_type_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="\ud83d\udcb0 Paid", callback_data="script_type_paid")],
        [InlineKeyboardButton(text="\ud83c\udd93 Free", callback_data="script_type_free")]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
