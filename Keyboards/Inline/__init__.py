from .confirm import ikb_confirm
from .courses_all import ikb_all_courses, ikb_on_course, ikb_off_course, ikb_individual
from .courses_my import ikb_courses_my, ikb_course_my_navigation
from .main_menu import ikb_start
from .notification import ikb_notification, ikb_user_notification
from .my_settings import ikb_settings, ikb_links
from .tasks import ikb_select_type, ikb_select_level, ikb_select_task

__add__ = ['ikb_confirm', 'ikb_all_courses', 'ikb_on_course', 'ikb_off_course', 'ikb_individual',
           'ikb_settings', 'ikb_links', 'ikb_courses_my', 'ikb_course_my_navigation',
           'ikb_select_type', 'ikb_select_level', 'ikb_select_task',
           'ikb_notification', 'ikb_user_notification']
