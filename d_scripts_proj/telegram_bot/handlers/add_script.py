import aiohttp
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

from states import AddScriptStates
from keyboards import script_type_keyboard

router = Router()

# This command requires authentication, which is handled by the AuthMiddleware
@router.message(Command("addscript"))
async def add_script_start(message: Message, state: FSMContext):
    await state.set_state(AddScriptStates.waiting_for_title)
    await message.answer("Let's add a new script. First, enter the <b>title</b>:")

@router.message(AddScriptStates.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddScriptStates.waiting_for_description)
    await message.answer("Great. Now, enter the <b>description</b>:")

@router.message(AddScriptStates.waiting_for_description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(AddScriptStates.waiting_for_type)
    await message.answer("Got it. Is the script <b>Paid</b> or <b>Free</b>?", reply_markup=script_type_keyboard())

@router.callback_query(F.data.startswith("script_type_"), AddScriptStates.waiting_for_type)
async def process_script_type(callback: types.CallbackQuery, state: FSMContext):
    script_type = callback.data.split("_")[2]
    await callback.answer()
    
    if script_type == "free":
        await state.update_data(price=0.00)
        await state.set_state(AddScriptStates.waiting_for_video_url)
        await callback.message.answer("Script set to Free. Now, please enter a <b>video demonstration URL</b> (e.g., from YouTube). You can type 'skip' if there is no video.")
    else:
        await state.set_state(AddScriptStates.waiting_for_price)
        await callback.message.answer("Script set to Paid. Please enter the <b>price</b> (e.g., 9.99):")

@router.message(AddScriptStates.waiting_for_price)
async def process_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
        if price <= 0:
            raise ValueError
        await state.update_data(price=f"{price:.2f}")
        await state.set_state(AddScriptStates.waiting_for_video_url)
        await message.answer("Price set. Finally, enter the <b>video demonstration URL</b>. You can type 'skip' to leave it empty.")
    except (ValueError, TypeError):
        await message.answer("Invalid price format. Please enter a number greater than 0, like <b>15.50</b>.")

@router.message(AddScriptStates.waiting_for_video_url)
async def process_video_and_create(message: Message, state: FSMContext, config):
    video_url = message.text
    if video_url.lower() != 'skip':
        await state.update_data(video_url=video_url)
    else:
        await state.update_data(video_url="")

    data = await state.get_data()
    api_url = f"{config.BACKEND_API_URL}/api/scripts/"
    headers = {"Authorization": f"Bearer {data.get('jwt_token')}"}
    
    payload = aiohttp.FormData()
    payload.add_field('title', data['title'])
    payload.add_field('description', data['description'])
    payload.add_field('price', str(data['price']))
    if data.get('video_url'):
        payload.add_field('video_url', data['video_url'])

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, data=payload, headers=headers) as response:
                if response.status == 201:
                    await message.answer("\u2705 Script successfully added to the catalog!")
                else:
                    response_text = await response.text()
                    await message.answer(f"\u274c <b>Error adding script.</b>\nStatus: {response.status}\nResponse: <code>{response_text}</code>")
    except aiohttp.ClientError as e:
        await message.answer(f"\u274c <b>Connection error.</b> Could not connect to the backend API.\nDetails: <code>{e}</code>")

    await state.clear()
