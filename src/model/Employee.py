
class Employee:
    total_employees = 0
    emp_index = -1

    def __init__(self, name: str, id: str, departments: list[int], weekly_hrs: int, exp_lvl: int, pref = None):
        self.name = name # name of employee
        self.id = id # id/tag to reference them by
        self.departments = departments # list of departments the employee works in
        self.weekly_hrs = weekly_hrs # amount of hours one should work weekly according to contract
        self.exp_lvl = exp_lvl # experience level of the employee where 1 is "provides experience" and 2 is "needs experience"
        self.pref = pref # list of preferences regarding working days
        Employee.total_employees += 1
        self.emp_index = Employee.total_employees-1

    def __str__(self):
        s = f"name: {self.name}, id: {self.id}, dep: ["
        for i in range(len(self.departments)):
            if self.departments[i] == 0:
                s += "labor"
            if self.departments[i] == 1:
                s += "maternity"
            if i == len(self.departments)-1:
                s += "], "
            else:
                s += ", "
        s += f"weekly_hrs: {self.weekly_hrs}, exp_lvl: {self.exp_lvl}\n"
        if self.pref is not None:
            for p in self.pref:
                s += f"\t{p}\n"
        return s