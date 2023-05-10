from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputMediaPhoto, Message, CallbackQuery

from Classes import MyMessage, User, Task
from Keyboards import ikb_select_type, ikb_select_level, ikb_select_task, ikb_confirm, kb_new_task, kb_control
from Keyboards.Callback import cb_menu, navigation, confirm
from loader import dp, bot, tasks_db
from temp import POSTERS


class NewTask(StatesGroup):
    task_type = State()
    task_level = State()
    task_value = State()
    task_confirm = State()


@dp.callback_query_handler(navigation.filter(menu='types'))
async def select_tasks_type(_, msg: MyMessage, user: User):
    poster = POSTERS.get('task_main')
    caption = f'{user.name}, выбери тему задач!'
    btn_list = [btn[0] for btn in set(tasks_db.collect())]
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id, message_id=msg.message_id,
                                 reply_markup=ikb_select_type(btn_list, user))


@dp.callback_query_handler(navigation.filter(menu='level'))
async def select_tasks_level(_, user: User, msg: MyMessage):
    btn_list = [btn[0] for btn in set(tasks_db.collect(msg.type))]
    btn_list = [btn for btn in ['easy', 'normal', 'hard'] if btn in btn_list]
    poster = POSTERS.get('task_main')
    caption = f'{user.name}, выбери уровень сложности!'
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id, message_id=msg.message_id,
                                 reply_markup=ikb_select_level(btn_list, msg.type))


@dp.callback_query_handler(navigation.filter(menu='task'))
async def select_tasks_level(_, user: User, msg: MyMessage):
    tasks_list = tasks_db.collect(msg.type, msg.level)
    current_task = Task(tasks_list[msg.id])
    poster = current_task.poster
    caption = f'{msg.id + 1}/{len(tasks_list)}\n\n{current_task.value}'
    await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
                                 chat_id=msg.chat_id, message_id=msg.message_id,
                                 reply_markup=ikb_select_task(len(tasks_list), user, msg))


# @dp.callback_query_handler(navigation.filter(menu='level'))
# async def select_tasks(_, msg: MyMessage, user: User):
#     task_list = tasks_db.collect(msg.type, msg.level)
#     current_task = Task(task_list[msg.id])
#     poster = current_task.poster
#     caption = f'{msg.id + 1}/{len(task_list)}\n\n{current_task.value}'
#     await bot.edit_message_media(media=InputMediaPhoto(media=poster, caption=caption),
#                                  chat_id=msg.chat_id, message_id=msg.message_id,
#                                  reply_markup=ikb_select_task('level', user, task_list, msg))
#
#
@dp.callback_query_handler(cb_menu.filter(button='add_task'))
async def add_task_command(message: Message):
    await bot.send_message(message.from_user.id, text='Введите тип задачи или введите новый:',
                           reply_markup=kb_new_task())
    await NewTask.task_type.set()


@dp.message_handler(state=NewTask.task_type)
async def input_task_type(message: Message, state: FSMContext):
    await state.update_data({'task_type': message.text})
    await message.answer(text='Введите сложность задачи:', reply_markup=kb_new_task(True))
    await NewTask.next()


@dp.message_handler(state=NewTask.task_level)
async def input_task_level(message: Message, state: FSMContext):
    if message.text in ['easy', 'normal', 'hard']:
        await state.update_data({'task_level': message.text})
        await message.answer(text='Введите условие задачи:', reply_markup=kb_control(True))
        await NewTask.next()
    else:
        await message.answer(text='Введите сложность задачи:', reply_markup=kb_new_task(True))


@dp.message_handler(state=NewTask.task_value)
async def task_confirm(message: Message, state: FSMContext):
    await state.update_data({'task_value': message.text})
    data = await state.get_data()
    caption = f'Тип задачи: {data.get("task_type")}\nСложность: {data.get("task_level")}' \
              f'\nУсловие: {data.get("task_value")}\n\nСохранить?'
    await message.answer(text=caption, reply_markup=ikb_confirm('new_task'))
    await NewTask.next()


@dp.callback_query_handler(confirm.filter(menu='new_task'), state=NewTask.task_confirm)
async def start_command(call: CallbackQuery, msg: MyMessage, state: FSMContext):
    if msg.confirm:
        data = await state.get_data()
        try:
            tasks_db.add((data.get("task_type"), data.get("task_level"), data.get("task_value")))
            await call.answer('Задача добавлена', show_alert=True)
        except:
            await call.answer('Ошибка добавления', show_alert=True)
        # user_list = [user[0] for user in users_db.select(alerts_news='True')]
        # for user in user_list:
        #     try:
        #         await bot.send_message(user,
        #                                f'Добавлена новая задача на {data.get("task_type")}, сложности {data.get("task_level")}')
        #     except:
        #         print('Юзер не в ресурсе')
    else:
        await call.answer('Отмена')
    await state.reset_data()
    await state.finish()


@dp.callback_query_handler(navigation.filter(menu='task_delete'))
async def add_task_command(_, msg: MyMessage):
    task_id = tasks_db.select(msg.type, msg.level)[msg.id][0]
    await bot.send_message(msg.chat_id, text='Точно удалить задачу?',
                           reply_markup=ikb_confirm('delete', task_id))


@dp.callback_query_handler(confirm.filter(menu='delete'))
async def add_task_command(call: CallbackQuery, msg: MyMessage):
    if msg.confirm:
        tasks_db.delete(int(msg.args))
        await call.answer('Задача удалена', show_alert=True)
    await bot.send_message(msg.chat_id, text='Возврат в главное меню /start')
