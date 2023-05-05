from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from loader import dp
from .start import cmd_start


@dp.message_handler(Text(equals='Отмена'), content_types=['text', 'photo'], state='*')
async def cancel_fsm(message: Message, state: FSMContext):
    await state.reset_state()
    await state.finish()
    await cmd_start(message)
