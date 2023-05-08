class User:
    def __init__(self, user_data: tuple[int, int, int, int, int, int, str, str], name: str):
        _, tg_id, admin, alert_stream, alert_course, alert_news, courses, lectures = user_data
        self.id = tg_id
        self.name = name
        self._admin = admin
        self.alert_stream = alert_stream
        self.alert_course = alert_course
        self.alert_news = alert_news
        self.courses = courses.split() if courses else courses
        self.lectures = lectures.split() if lectures else lectures

    @property
    def is_admin(self) -> bool:
        return True if self._admin else False

    @property
    def is_active_admin(self) -> bool:
        return True if self._admin == 1 else False

    def alert(self, alert_type: str):
        match alert_type:
            case 'stream':
                return True if self.alert_stream else False
        match alert_type:
            case 'course':
                return True if self.alert_course else False
        match alert_type:
            case 'news':
                return True if self.alert_news else False
