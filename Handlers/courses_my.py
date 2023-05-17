from aiogram.types import InputMediaPhoto

from Classes import MyMessage, User, Lecture
from Keyboards import ikb_courses_my, ikb_course_my_navigation
from Keyboards.Callback import cb_menu, course_navigation
# from Misc import MsgToDict, Course, PICTURES
from loader import dp, bot, courses_db, users_db
from temp import POSTERS


@dp.callback_query_handler(cb_menu.filter(button='courses_my'))
async def check_course_or_lecture(_, msg: MyMessage, user: User):
    courses, lectures = users_db.courses_and_lectures(user.id)
    if courses:
        courses = [course for course in courses.split()]
    else:
        courses = []
    # if lectures:
    #     lectures = [courses_db.lecture(lecture.split(':')[0], False, int(lecture.split(':')[1]))
    #                 for lecture in lectures.split()]
    # else:
    #     lectures = []

    # courses = [Course(courses_db.select(table=course)) for course in courses.split()] if courses else []
    # lectures_list = Course(
    #     (None, 'Отдельные лекции', 'custom', 'Лекции приобретенные поштучно', POSTERS.get('all_courses'),
    #      None, None, None, None, False))
    # if lectures:
    #     [lectures_list.add_new(lecture) for lecture in lectures.split()]
    # courses_list.append(lectures_list)
    #
    poster = POSTERS.get('courses_my')
    caption = f'{user.name}, это твои курсы!' if courses or lectures else f'{user.name}, у тебя нет активных курсов!'
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id,
                                 message_id=msg.message_id,
                                 reply_markup=ikb_courses_my(courses, lectures))


@dp.callback_query_handler(course_navigation.filter(menu='courses_my'))
async def users_courses(_, msg: MyMessage, user: User):
    if msg.table != 'custom':
        cur_course = courses_db.lecture(msg.table, True)
    else:
        _, lectures = users_db.courses_and_lectures(user.id)
        cur_course = [courses_db.lecture(lecture.split(':')[0], False, int(lecture.split(':')[1]))
                      for lecture in lectures.split()]
    cur_lecture = Lecture(cur_course[msg.id], msg.table)
    poster = cur_lecture.poster if cur_lecture.is_finished else POSTERS.get('no_lecture')
    caption = f'{msg.id + 1}/{len(cur_course)}\n{cur_lecture.info(False)}'
    # buttons = (cur_lecture.lect_url, cur_lecture.semi_url, cur_lecture.comp_url)

    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id,
                                 message_id=msg.message_id,
                                 reply_markup=ikb_course_my_navigation('courses_my', cur_lecture, msg.id,
                                                                       len(cur_course), msg.table))
