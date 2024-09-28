

class Employee:

    shifts = None

    def __init__(self, name: str, id: str, departments: list[str], weekly_hrs: int, preferences):
        self.name = name
        self.id = id
        self.departments = departments
        self.weekly_hrs = weekly_hrs
        self.preferences = preferences