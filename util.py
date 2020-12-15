class Vertex:
    def __init__(self, index, color=-1, degree=0):
        self.index = index
        self.color = color
        self.degree = degree

    def __repr__(self):
        return "Vertex({0},{1},{2})".format(self.index, self.color, self.degree)



class Edge:
    def __init__(self, a, b):
        a.degree += 1
        b.degree += 1
        self.a = a
        self.b = b


    def __repr__(self):
        return "Edge({0}, {1})".format(self.a, self.b)


class Graph:
    def __init__(self, v, e):
        self.V = set(v)
        self.E = set(e)

    def __repr__(self):
        return "Graph({0}, {1})".format(self.V, self.E)

    def __deepcopy__(self, memo):
        V = {v.index: Vertex(v.index, v.color) for v in self.V}
        E = [Edge(V[e.a.index], V[e.b.index]) for e in self.E]
        return Graph(V.values(), E)

    # Gets a vertex with given index if it exists, else return None.
    def GetVertex(self, i):
        for v in self.V:
            if v.index == i:
                return v
        return None

    # Returns the incident edges on a vertex.
    def IncidentEdges(self, v):
        return [e for e in self.E if (e.a == v or e.b == v)]


