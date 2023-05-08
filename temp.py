from Classes import Course
from loader import settings_db, courses_db

POSTERS = {}
LINKS = {}
# TASKS: dict[dict[str, list[str]]] = {}
# COURSES: dict[str, Course] = {}


def load_posters():
    global POSTERS
    data = settings_db.load('poster')
    for item in data:
        POSTERS[item[2]] = item[3]


def load_links():
    global LINKS
    data = settings_db.load('link')
    for item in data:
        LINKS[item[2]] = item[3]


# def load_tasks():
#     global TASKS
#     for task in tasks_db.collect():
#         task_type = TASKS.get(task[1], {})
#         if task_type:
#             level = task_type.get(task[2], [])
#             if level:
#                 level.append(task[3])
#             else:
#                 task_type[task[2]] = [task[3]]
#         else:
#             TASKS[task[1]] = {task[2]: [task[3]]}


def load_courses(full: bool = False):
    courses = {}
    data = courses_db.load()
    for course in data:
        courses[course[1]] = Course(course, full)
    return courses


def load_temp():
    load_posters()
    load_links()
    # load_courses()
    # load_tasks()
