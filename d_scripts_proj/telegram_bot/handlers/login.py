import aiohttp
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()

@router.message(Command("login"))
async def cmd_login(message: Message, command: Command, state: FSMContext, config):
    if not command.args:
        await message.answer(
            "Please provide username and password.\n"
            "Usage: <code>/login your_username your_password</code>"
        )
        return

    try:
        username, password = command.args.split(maxsplit=1)
    except ValueError:
        await message.answer(
            "Incorrect format. Please use:\n"
            "<code>/login your_username your_password</code>"
        )
        return
    
    api_url = f"{config.BACKEND_API_URL}/api/auth/login/"
    payload = {
        'username': username,
        'password': password
    }
    
    await message.answer("Attempting to log in...")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    # We only need the access token for API calls
                    jwt_token = data.get('access')
                    await state.update_data(jwt_token=jwt_token, username=username)
                    await message.answer(f"\u2705 Login successful! Welcome, <b>{username}</b>.")
                elif response.status == 401:
                    await message.answer("\u274c Login failed. Invalid credentials.")
                else:
                    await message.answer(f"\u274c An error occurred. Status: {response.status}")
    except aiohttp.ClientError as e:
        await message.answer(f"\u274c Connection error. Could not reach the backend API.\nDetails: {e}")
