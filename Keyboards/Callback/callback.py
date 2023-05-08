from aiogram.utils.callback_data import CallbackData

cb_menu = CallbackData('menu', 'name', 'button')
navigation = CallbackData('navigation', 'menu', 'type', 'level', 'id')
course_navigation = CallbackData('course_navigation', 'menu', 'table', 'current_id')

confirm = CallbackData('confirm', 'menu', 'args', 'button')



list_navigation = CallbackData('list_navigation', 'menu', 'task_type', 'task_level', 'current_id')
settings = CallbackData('settings_option', 'menu', 'button')