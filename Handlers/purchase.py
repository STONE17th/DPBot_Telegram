from os import getenv
from aiogram.types import Message, PreCheckoutQuery, LabeledPrice, ContentType

from Classes import MyMessage, User
from Keyboards.Callback import course_navigation
from loader import dp, users_db
from temp import load_courses


@dp.callback_query_handler(course_navigation.filter(menu='purchase'))
async def purchase(_, msg: MyMessage):
    all_courses = load_courses()
    if msg.id == -1:
        target = all_courses.get(msg.table)
        my_purchase = msg.table
    else:
        target = all_courses.get(msg.table).lecture[msg.id]
        my_purchase = f'{msg.table}:{msg.id + 1}'
    prices = [LabeledPrice(label=target.name, amount=target.price * 100)]
    await dp.bot.send_invoice(chat_id=msg.chat_id,
                              title=all_courses.get(msg.table).name,
                              description=target.name,
                              provider_token=getenv('P_TOKEN'),
                              currency='RUB',
                              prices=prices,
                              payload=my_purchase,
                              start_parameter='purchase')

    @dp.pre_checkout_query_handler()
    async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
        await dp.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

    @dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
    async def process_pay(message: Message, user: User):
        my_buy = message.successful_payment.invoice_payload
        users_db.purchase(user.id, my_buy)
        txt = 'лекции'if ':' in my_buy else 'курсу'
        await message.answer(text=f'Спасибо за покупку!\nДоступ к {txt}'
                                  f'будет во вкладке "Мои курсы"\n\n'
                                  f'Вернуться в главное меню /start')