

class Shift:

    def __init__(self, start_time: int, end_time: int, day=None):
        self.start_time = start_time # start time of shift
        self.end_time = end_time # end time of shift
        self.day = day # day of the shift
    
    
    def calc_hours(self) -> int:
        "Calculates length of a shift based on start time and end time"
        if self.end_time > self.start_time:
            return self.end_time-self.start_time
        else:
            return 24-self.start_time + self.end_time