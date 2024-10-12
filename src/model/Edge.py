
class Edge:
    total_edges = 0
    def __init__(self, type, frm, to, cap_forward: int, counterpart = None, weight: int = 0, lower_bound: int = 0, must_take: bool = False, flow: int = 0):
        self.type = type # forward: 0, backward: 1
        self.frm = frm # the "from" vertex
        self.to = to # the "to" vertex
        self.cap_forward = cap_forward # the capacity in the forward direction
        self.counterpart = counterpart # the edge in opposite direction
        self.weight = weight # the weight signifying desire
        self.lower_bound = lower_bound # lower bound capacity signifying a minimal amount of flow if edge is to be taken
        self.must_take = must_take # bollean which states whether an edge is required to be taken
        self.flow = flow
        Edge.total_edges += 1

    def connect_to_vertex(self, vertex):
        self.to = vertex

    def connect_from_vertex(self, vertex):
        self.frm = vertex
    
    def add_flow(self, flow):
        if self.type == 0:
            self.flow += flow
            # if self.frm.purpose != 0 and self.to.purpose != 7:
            self.counterpart.cap_forward += flow
        elif self.type == 1:
            self.cap_forward -= flow
            self.counterpart.flow -= flow

    def __str__(self):
        return f"{self.frm} -- ({self.flow}/{self.cap_forward}, {self.weight}) --> {self.to}"