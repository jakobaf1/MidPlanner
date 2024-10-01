import Vertex

class Edge:

    def __init__(self, frm: Vertex, to: Vertex, cap_forward: int, cap_backward: int, weight: int):
        self.frm = frm # the "from" vertex
        self.to = to # the "to" vertex
        self.cap_forward = cap_forward # the capacity in the forward direction
        self.cap_backward = cap_backward # the capacity in backwards direction
        self.weight = weight # the weight signifying desire

    def connect_to_vertex(self, vertex):
        self.to = vertex

    def connect_from_vertex(self, vertex):
        self.frm = vertex