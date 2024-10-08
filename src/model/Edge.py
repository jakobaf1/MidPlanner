
class Edge:

    def __init__(self, frm, to, cap_forward: int, cap_backward: int = 0, weight: int = 0, lower_bound: int = 0, must_take: bool = False, flow: int = 0):
        self.frm = frm # the "from" vertex
        self.to = to # the "to" vertex
        self.cap_forward = cap_forward # the capacity in the forward direction
        self.cap_backward = cap_backward # the capacity in backwards direction
        self.weight = weight # the weight signifying desire
        self.lower_bound = lower_bound # lower bound capacity signifying a minimal amount of flow if edge is to be taken
        self.must_take = must_take # bollean which states whether an edge is required to be taken
        self.flow = flow

    def connect_to_vertex(self, vertex):
        self.to = vertex

    def connect_from_vertex(self, vertex):
        self.frm = vertex
    
    def add_flow(self, flow):
        self.flow += flow

    def __str__(self):
        return f"{self.frm} -- ({self.flow}/{self.cap_forward}, {self.weight}) --> {self.to}"