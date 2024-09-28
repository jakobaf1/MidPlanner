import Vertex

class Edge:

    def __init__(self, to: Vertex, from_: Vertex, cap_forward: int, cap_backward: int, weight: int):
        self.to = to
        self.from_ = from_
        self.cap_forward = cap_forward
        self.cap_backward = cap_backward
        self.weight = weight

  