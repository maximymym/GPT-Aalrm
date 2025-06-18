from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message
from aiogram.fsm.context import FSMContext

from config import settings

class AuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        
        state: FSMContext = data.get('state')
        user_data = await state.get_data()
        
        # Pass config object to all handlers
        data['config'] = settings

        # Allow /addscript to start the FSM sequence
        # The check will happen at the end when data is submitted
        if isinstance(event, Message) and event.text and event.text.startswith('/addscript'):
            if not user_data.get('jwt_token'):
                 await event.answer("Access denied. \ud83d\udeab\nPlease /login first.")
                 return
        
        return await handler(event, data)
