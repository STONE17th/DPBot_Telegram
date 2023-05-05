from aiogram.types import InputMediaPhoto

from Classes import MyMessage, User
from Keyboards import ikb_all_courses, ikb_on_course, ikb_off_course
from Keyboards.Callback import cb_menu, course_navigation
from loader import dp, bot
from temp import POSTERS, COURSES


@dp.callback_query_handler(cb_menu.filter(button='courses_all'))
async def menu_courses_all(_, user: User, msg: MyMessage):
    poster = POSTERS.get('courses_all')
    caption_empty = f'{user.name}, пока нам нечего тебе предложить. Возвращайся позже...'
    caption = f'{user.name}, если лекция "Онлайн", то ее можно купить только полностью и присоединиться к идущему ' \
              f'курсу. В завершенных курсах можно купить отдельные лекции'
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption if COURSES else caption_empty),
                                 chat_id=msg.chat_id, message_id=msg.message_id,
                                 reply_markup=ikb_all_courses(user.is_admin))


@dp.callback_query_handler(course_navigation.filter(menu='online'))
async def menu_courses_all(_, user: User, msg: MyMessage):
    course = COURSES.get(msg.table)
    if user.is_admin:
        poster = course.poster
        lecture = course.lecture[msg.id]
        caption = lecture.info(True)
        await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                     chat_id=msg.chat_id, message_id=msg.message_id,
                                     reply_markup=ikb_off_course(user, 'offline', msg.table, msg.id))
    else:
        poster = course.poster
        lecture = course.lecture[msg.id]
        caption = lecture.info()
        await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                     chat_id=msg.chat_id, message_id=msg.message_id,
                                     reply_markup=ikb_on_course(user, msg.table))


@dp.callback_query_handler(course_navigation.filter(menu='offline'))
async def menu_courses_all(_, user: User, msg: MyMessage):
    course = COURSES.get(msg.table)
    if user.is_admin:
        poster = course.poster
        lecture = course.lecture[msg.id]
        caption = lecture.info(True)
        await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                     chat_id=msg.chat_id, message_id=msg.message_id,
                                     reply_markup=ikb_off_course(user, 'offline', msg.table, msg.id))
    else:
        poster = course.poster
        lecture = course.lecture[msg.id]
        caption = lecture.info()
        await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                     chat_id=msg.chat_id, message_id=msg.message_id,
                                     reply_markup=ikb_on_course(user, msg.table))