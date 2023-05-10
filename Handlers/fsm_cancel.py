from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from loader import bot, dp
from temp import POSTERS
from Keyboards import ikb_main


@dp.message_handler(Text(equals='Отмена'), content_types=['text', 'photo'], state='*')
async def cancel_fsm(message: Message, state: FSMContext):
    poster = POSTERS.get('cancel')
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_photo(message.from_user.id, photo=poster, caption='Ввод отменен', reply_markup=ikb_main())
    await state.reset_state()
    await state.finish()
