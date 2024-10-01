

class Shift:

    def __init__(self, start_time: int, end_time: int, day):
        self.start_time = start_time # start time of shift
        self.end_time = end_time # end time of shift
        self.day = day # day of the shift
    
    
    def calc_hours(start: int, end: int) -> int:
        "Calculates length of a shift based on start time and end time"
        if end > start:
            return end-start
        else:
            return 24-start + end