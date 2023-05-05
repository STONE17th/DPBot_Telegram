from loader import settings_db, courses_db
from Classes import Course
POSTERS = {}
LINKS = {}
COURSES: dict[str, Course] = {}


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


def load_courses():
    global COURSES
    data = courses_db.load()
    for course in data:
        COURSES[course[1]] = Course(course)
