from Shift import Shift

class Preference:
    
    def __init__(self, wanted, pref_lvl: int, date = None, day = None, shift = None, repeat = False, repeat_pattern = None, repeat_duration = None) -> None:
        self.wanted = wanted  # boolean, true for wanted, false for not
        self.pref_lvl = pref_lvl # pref level between 1-5. 1 is hard constraint, 2-5 are soft with varying weights
        self.date = date  # optional date field (YYYY-MM-DD format)
        self.day = day  # optional day of the week (e.g., "Monday")
        self.shift = shift  # optional shift (e.g., "15-23")
        self.repeat = repeat  # boolean, whether to repeat
        self.repeat_pattern = repeat_pattern  # (is weekly by default) e.g., 'weekly' or 'monthly'
        self.repeat_duration = repeat_duration  # optional, duration of repetition (e.g., 4 weeks)