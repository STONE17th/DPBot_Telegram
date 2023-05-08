from aiogram.types import Message, CallbackQuery


class MyMessage:
    def __init__(self, update: Message | CallbackQuery):
        self.chat_id = update.from_user.id
        if isinstance(update, Message):
            self.message_id = update.message_id
            self.data = update.text
        elif isinstance(update, CallbackQuery):
            self.message_id = update.message.message_id
            self.data = update.data.split(':')
            if self.data:
                match self.data:
                    case ['navigation', menu, task_type, task_level, current_id]:
                        self.menu = menu
                        self.type = task_type
                        self.level = task_level
                        self.id = int(current_id)
                    case ['course_navigation', _, table, lecture_id]:
                        self.table = table
                        self.id = int(lecture_id)
                    case [_, 'settings', button]:
                        # self.menu = name
                        self.button = button
                    case ['confirm', menu, args, button]:
                        self.menu = menu
                        self.args = args
                        self.confirm = True if button == 'yes' else False
                    case _:
                        self.data = update.data
