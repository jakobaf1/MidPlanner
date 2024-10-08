
class Preference:
    
    def __init__(self, wanted=None, pref_lvl: int=None, date = None, day = None, shift = None, repeat = None, repeat_pattern = None, repeat_duration = None) -> None:
        self.wanted = wanted  # boolean, true for wanted, false for not
        self.pref_lvl = pref_lvl # pref level between 1-5. 1 is hard constraint, 2-5 are soft with varying weights
        self.date = date  # optional date field (YYYY-MM-DD format)
        self.day = day  # optional day of the week (e.g., "Monday")
        self.shift = shift  # optional shift (e.g., "15-23")
        self.repeat = repeat   # 'daily'=0, 'weekly'=1, 'odd'=2, 'even'=3, 'tri'=4 or 'monthly'=5
        self.repeat_duration = repeat_duration  # optional, duration of repetition (e.g., 4 weeks)

    def __str__(self):
        return f"wanted: {self.wanted}, pref_lvl: {self.pref_lvl}, date: {self.date}, day: {self.day}, shift: {self.shift}, repeat: {self.repeat}"