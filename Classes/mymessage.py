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
                    case ['list_navigation', _, task_type, level, current_id]:
                        self.type = task_type
                        self.level = level
                        self.id = int(current_id)
                    case ['course_navigation', _, table, lecture_id]:
                        self.table = table
                        self.id = int(lecture_id)
                    case ['settings_option', menu, button]:
                        self.menu = menu
                        self.button = button
                    case ['confirm', menu, args, button]:
                        self.menu = menu
                        self.args = args
                        self.confirm = True if button == 'yes' else False
                    case _:
                        self.data = update.data
