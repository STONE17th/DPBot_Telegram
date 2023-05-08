from temp import POSTERS


class Task:
    def __init__(self, task: tuple):
        _, task_type, task_level, task_value = task
        self.type = task_type
        self.level = task_level
        self.value = task_value
        self.poster = POSTERS.get(f'task_{task_level}')
