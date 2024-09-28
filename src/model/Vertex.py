from Edge import Edge
from Employee import Employee
from Shift import Shift

class Vertex:

    def __init__(self, day: int, employee: Employee, shift: Shift, inGoing: Edge, outGoing: Edge):
        self.day = day