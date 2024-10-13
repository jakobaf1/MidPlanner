
class Vertex:
    total_vertices = 0
    vertex_index = -1
    # Constructor with optional parameters for all use cases (source/sink, shifts, employees, day/eve/night etc..)
    def __init__(self, in_going = None, out_going = None, purpose: int = None, 
                 day: int = None, employee = None, shift = None, time_of_day = None, 
                 department = None, experience = None, name = None):
        self.in_going = in_going if in_going is not None else [] # edges which go into the vertex
        self.out_going = out_going if out_going is not None else []
        self.day = day # used if the vertex portrays a feature on a certain day
        # leading to different ways of handling using switch cases (0-7 for the 8 different nodes)
        self.purpose = purpose # int signifying the function of the node based on which layer in the graph it is in
        self.employee = employee # used if the vertex denotes an employee
        self.shift = shift # used if vertex denotes a shift
        self.timeOfDay = time_of_day # used if the vertex denotes one of the three periods within a day (day, eve, night)
        self.department = department # used for a vertex denoting department
        self.experience = experience # used for vertices which denote experience level
        self.name = name # Only used for debugging in order to see which nodes are which
        Vertex.total_vertices += 1
        self.vertex_index = Vertex.total_vertices-1
 
    def add_in_going(self, edge):
        self.in_going.append(edge)

    def add_out_going(self, edge):
        self.out_going.append(edge)

    def __str__(self):
        # can be modified later
        if self.purpose == 5:
            match self.name:
                case "0_0_0":
                    return "( day_lab_1 )"
                case "0_0_1":
                    return "( day_lab_2 )"
                case "0_1_0":
                    return "( day_mat_1 )"
                case "0_1_1":
                    return "( day_mat_2 )"
                case "1_0_0":
                    return "( eve_lab_1 )"
                case "1_0_1":
                    return "( eve_lab_2 )"
                case "1_1_0":
                    return "( eve_mat_1 )"
                case "1_1_1":
                    return "( eve_mat_2 )"
                case "2_0_0":
                    return "( night_lab_1 )"
                case "2_0_1":
                    return "( night_lab_2 )"
                case "2_1_0":
                    return "( night_mat_1 )"
                case "2_1_1":
                    return "( night_mat_2 )"
        elif self.purpose == 6:
                if "0_0" in self.name:
                    return f"( lab_day{self.name[3:]} )"
                if "0_1" in self.name:
                    return f"( lab_eve{self.name[3:]} )"
                if "0_2" in self.name:
                    return f"( lab_night{self.name[3:]} )"
                if "1_0" in self.name:
                    return f"( mat_night{self.name[3:]} )"
                if "1_1" in self.name:
                    return f"( mat_night{self.name[3:]} )"
                if "1_2" in self.name:
                    return f"( mat_night{self.name[3:]} )"
        return f"( {self.name} )"