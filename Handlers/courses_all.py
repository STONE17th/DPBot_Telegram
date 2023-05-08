from aiogram.types import InputMediaPhoto, CallbackQuery

from Classes import MyMessage, User
from Keyboards import ikb_all_courses, ikb_on_course, ikb_off_course, ikb_individual
from Keyboards.Callback import cb_menu, course_navigation
from loader import dp, bot, courses_db
from temp import POSTERS, load_courses


@dp.callback_query_handler(cb_menu.filter(button='courses_all'))
async def menu_courses_all(_, user: User, msg: MyMessage):
    poster = POSTERS.get('courses_all')
    caption_empty = f'{user.name}, пока нам нечего тебе предложить. Возвращайся позже...'
    caption = f'{user.name}, если лекция "Онлайн", то ее можно купить только полностью и присоединиться к идущему ' \
              f'курсу. В завершенных курсах можно купить отдельные лекции'
    all_courses = load_courses()
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption if all_courses else caption_empty),
                                 chat_id=msg.chat_id, message_id=msg.message_id,
                                 reply_markup=ikb_all_courses(user.is_active_admin))


@dp.callback_query_handler(course_navigation.filter(menu='online'))
async def menu_courses_all(_, user: User, msg: MyMessage):
    all_courses = load_courses()
    course = all_courses.get(msg.table)
    # if user.is_admin:
    #     poster = course.poster
    #     lecture = course.lecture[msg.id]
    #     caption = course.info(True) + '\n\n' + course.progress
    #     await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
    #                                  chat_id=msg.chat_id, message_id=msg.message_id,
    #                                  reply_markup=ikb_off_course(user, 'offline', msg.table, msg.id))
    # else:
    # lecture = course.lecture[msg.id]
    poster = course.poster
    caption = course.info() + '\n\n' + course.progress
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id, message_id=msg.message_id,
                                 reply_markup=ikb_on_course(user, msg.table))


@dp.callback_query_handler(course_navigation.filter(menu='offline'))
async def menu_courses_all(_, user: User, msg: MyMessage):
    all_courses = load_courses(user.is_active_admin)
    course = all_courses.get(msg.table)
    # if user.is_admin:
    lecture = course.lecture[msg.id]
    poster = lecture.poster
    caption = f'{msg.id + 1}/{course.quantity}\n' + lecture.info(True)
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id, message_id=msg.message_id,
                                 reply_markup=ikb_off_course(user, 'offline', msg.table, msg.id))
    # else:
    #     poster = course.poster
    #     lecture = course.lecture[msg.id]
    #     caption = f'{msg.id + 1}/{course.quantity}\n' + lecture.info()
    #     await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
    #                                  chat_id=msg.chat_id, message_id=msg.message_id,
    #                                  reply_markup=ikb_on_course(user, msg.table))


@dp.callback_query_handler(course_navigation.filter(menu='finalize_course'))
async def finalize_course(_, msg: MyMessage, user: User):
    courses_db.finalize(msg.table)
    all_courses = load_courses()
    poster = all_courses.get(msg.table).lecture[msg.id].poster
    caption = f'Курс {all_courses.get(msg.table).name} ' + ('финализирован' if COURSES.get(msg.table).finished < 2
                                                        else 'заархивирован')
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id, message_id=msg.message_id,
                                 reply_markup=ikb_off_course(user, 'offline', msg.table, msg.id))


@dp.callback_query_handler(cb_menu.filter(button='individual'))
async def individual_courses(_, user: User, msg: MyMessage):
    poster = POSTERS.get('individual_courses')
    caption = f'{user.name}, если ты здесь, то видимо тебе нужны индивидуальные курсы\n' \
              f'и , да,  мы можем с тобой поработать\nСамый главный вопрос который интересует всех - ' \
              f'СКОЛЬКО? тут нет однозначного ответа, зависит от того, чем будем заниматься :)\n' \
              f'Так что давай решим этот вопрос при личном общении.\n' \
              f'Жми кнопку "Оставить заявку" и я с тобой свяжусь. Гуд ЛАК!'
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id, message_id=msg.message_id,
                                 reply_markup=ikb_individual())


@dp.callback_query_handler(course_navigation.filter(menu='want'))
async def want_button(call: CallbackQuery, user: User):
    mention = "[" + user.name + "](tg://user?id=" + str(user.id) + ")"
    await bot.send_message(chat_id=409205647, text=f'{mention} хочет индивидуалочку! Отпишись ему!',
                           parse_mode='markdown')
    await call.answer(text='Заявка отправлена!\nСкоро ответит... Но это не точно :)', show_alert=True)
