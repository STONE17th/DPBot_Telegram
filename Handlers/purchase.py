from os import getenv

from aiogram.types import Message, PreCheckoutQuery, LabeledPrice, ContentType

from Classes import MyMessage, User, Course, Lecture
from Keyboards import ikb_purchase_done
from Keyboards.Callback import course_navigation
from loader import bot, dp, users_db, courses_db
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
        data = message.successful_payment.invoice_payload
        # try:
        users_db.purchase(user.id, data)
        txt = 'курса' if ':' not in data else 'лекции'
        purchase_data = [data.split(':')[0], int(data.split(':')[1])] if ':' in data else [data]
        my_product = courses_db.my_purchase(*purchase_data)
        my_product = Lecture(my_product, purchase_data[0]) if ':' in data else Course(my_product)
        poster = my_product.poster
        caption = f'Поздравляем с приобретением ' + txt + f' "{my_product.name}"\n' + \
                  f'\nДоступ к материалам {txt} открыт во вкладке "Мои курсы"\n' + (
                      '' if ':' in data else 'Не забудь подписаться на рабочую группу в TG (кнопка ниже)')
        url = None if ':' in data else my_product.tg_url
        await bot.send_photo(message.from_user.id, photo=poster, caption=caption,
                             reply_markup=ikb_purchase_done(url))
