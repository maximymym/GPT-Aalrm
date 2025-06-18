from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Welcome to the <b>D-Scripts Admin Bot</b>!\n\n"
        "Here are the available commands:\n"
        "\u25b6\ufe0f /start - Show this welcome message\n"
        "\ud83d\udd11 /login <code>&lt;username&gt; &lt;password&gt;</code> - Log in to the system\n"
        "\u2795 /addscript - Add a new script to the catalog (login required)\n"
    )
