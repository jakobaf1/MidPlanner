
class Vertex:
    # Constructor with optional parameters for all use cases (source/sink, shifts, employees, day/eve/night etc..)
    def __init__(self, in_going = [], out_going = [], purpose: int = None, 
                 day: int = None, employee = None, shift = None, time_of_day = None, 
                 department = None, experience = None):
        self.in_going = in_going # edges which go into the vertex
        self.out_going = out_going # edges which go from the vertex
        self.day = day # used if the vertex portrays a feature on a certain day
        # leading to different ways of handling using switch cases (0-7 for the 8 different nodes)
        self.purpose = purpose # int signifying the function of the node based on which layer in the graph it is in
        self.employee = employee # used if the vertex denotes an employee
        self.shift = shift # used if vertex denotes a shift
        self.timeOfDay = time_of_day # used if the vertex denotes one of the three periods within a day (day, eve, night)
        self.department = department # used for a vertex denoting department
        self.experience = experience # used for vertices which denote experience level
 
    def add_in_going(self, edge):
        self.in_going.append(edge)

    def add_out_going(self, edge):
        self.out_going.append(edge)

    def __str__(self):
        # can be modified later
        return f"( {self.purpose} )"