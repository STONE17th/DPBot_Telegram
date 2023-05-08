from .kb_control import kb_control, kb_stream
from .new_task import kb_new_task
from .Inline import ikb_confirm, ikb_start, ikb_all_courses, ikb_on_course, ikb_off_course, ikb_individual, \
    ikb_settings, ikb_links, ikb_courses_my, ikb_course_my_navigation,\
    ikb_select_type, ikb_select_level, ikb_select_task, ikb_notification, ikb_user_notification

__add__ = ['kb_control', 'kb_stream', 'kb_new_task',
           'ikb_confirm', 'ikb_start',
           'ikb_all_courses', 'ikb_on_course', 'ikb_off_course',
           'ikb_individual', 'ikb_settings', 'ikb_links', 'ikb_courses_my', 'ikb_course_my_navigation',
           'ikb_select_type', 'ikb_select_level', 'ikb_select_task',
           'ikb_notification', 'ikb_user_notification']
