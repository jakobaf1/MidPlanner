
class Employee:

    shifts = None

    def __init__(self, name: str, id: str, departments: list[int], weekly_hrs: int, exp_lvl: int, pref = None):
        self.name = name # name of employee
        self.id = id # id/tag to reference them by
        self.departments = departments # list of departments the employee works in
        self.weekly_hrs = weekly_hrs # amount of hours one should work weekly according to contract
        self.exp_lvl = exp_lvl # experience level of the employee where 1 is "provides experience" and 2 is "needs experience"
        self.pref = pref # list of preferences regarding working days