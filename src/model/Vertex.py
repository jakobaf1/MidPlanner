from Edge import Edge
from Employee import Employee
from Shift import Shift

class Vertex:
    # Constructor with optional parameters for all use cases (source/sink, shifts, employees, day/eve/night etc..)
    def __init__(self, in_going: list[Edge] = None, out_going: list[Edge] = None, purpose: str = None, 
                 day: int = None, employee: Employee = None, shift: Shift = None, time_of_day = None, 
                 department = None, experience = None):
        if in_going == None: []  # sets the list to empty if no in_going is given
        else: self.in_going = in_going # edges which go into the vertex
        if out_going == None: []  # sets the list to empty if no out_going is given
        else: self.out_going = out_going # edges which go from the vertex
        self.day = day # used if the vertex portrays a feature on a certain day
        self.purpose = purpose # used to determine whether node is a sink or source
        self.employee = employee # used if the vertex denotes an employee
        self.shift = shift # used if vertex denotes a shift
        self.timeOfDay = time_of_day # used if the vertex denotes one of the three periods within a day (day, eve, night)
        self.department = department # used for a vertex denoting department
        self.experience = experience # used for vertices which denote experience level

    def add_in_going(self, edge):
        self.in_going.append(edge)

    def add_out_going(self, edge):
        self.out_going.append(edge)