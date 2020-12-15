import random
import itertools
import copy
import traceback
import sys
#import TyBot
import percolator
import time
#import SarahBot

class Vertex:
    def __init__(self, index, color=-1):
        self.index = index
        self.color = color

    def __repr__(self):
        if self.color == -1:
            return "Vertex({0})".format(self.index)
        else:
            return "Vertex({0}, {1})".format(self.index, self.color)


class Edge:
    def __init__(self, a, b):
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

    # Gets a vertex with given index if it exists, else return None.
    def GetVertex(self, i):
        for v in self.V:
            if v.index == i:
                return v
        return None

    # Returns the incident edges on a vertex.
    def IncidentEdges(self, v):
        return [e for e in self.E if (e.a == v or e.b == v)]

    # Returns the degree of the given vertex.
    def Degree(self, v):
        return len(self.IncidentEdges(v))

    # Returns all neighbors of the given vertex.
    def GetNeighbors(self, v):
        edges = self.IncidentEdges(v)
        return [u for u in self.V if Edge(u, v) in edges or Edge(v, u) in edges]

    # Removes the given vertex v from the graph, as well as the edges attached to it.
    # Removes all isolated vertices from the graph as well.
    def Percolate(self, v):
        # Get attached edges to this vertex, remove them.
        for e in self.IncidentEdges(v):
            self.E.remove(e)
        # Remove this vertex.
        self.V.remove(v)
        # Remove all isolated vertices.
        to_remove = {u for u in self.V if len(self.IncidentEdges(u)) == 0}
        self.V.difference_update(to_remove)

gui_enabled = True
if gui_enabled:
    import TyGUI
    gui = TyGUI.GUI()

# This is the main game loop.
def PlayGraph(s, t, graph):
    players = [s, t]
    active_player = 0

    # Phase 1: Coloring Phase
    while any(v.color == -1 for v in graph.V):
        # First, try to just *run* the player's code to get their vertex.
        try:
            chosen_vertex = players[active_player].ChooseVertexToColor(copy.copy(graph), active_player)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = graph.GetVertex(chosen_vertex.index)
            if not original_vertex:
                return 1 - active_player
            if original_vertex.color != -1:
                return 1 - active_player
            # If output is reasonable, color this vertex.
            original_vertex.color = active_player
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Swap current player.
        active_player = 1 - active_player
        if gui_enabled:
            gui.DrawGraph(graph, active_player)

    # Check that all vertices are colored now.
    assert all(v.color != -1 for v in graph.V)

    move_times = []

    # Phase 2: Removal phase
    # Continue while both players have vertices left to remove.
    while len([v for v in graph.V if v.color == active_player]) > 0:
        # First, try to just *run* the removal code.
        try:
            t0 = time.time()
            chosen_vertex = players[active_player].ChooseVertexToRemove(copy.copy(graph), active_player)
            move_times.append(time.time() - t0)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Next, check that their output was reasonable.
        try:
            original_vertex = graph.GetVertex(chosen_vertex.index)
            if not original_vertex:
                return 1 - active_player
            if original_vertex.color != active_player:
                return 1 - active_player
            # If output is reasonable, remove ("percolate") this vertex + edges attached to it, as well as isolated vertices.
            graph.Percolate(original_vertex)
        # Only case when this should fire is if chosen_vertex.index does not exist or similar error.
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            return 1 - active_player
        # Swap current player
        active_player = 1 - active_player
        if gui_enabled:
            gui.DrawGraph(graph, active_player)

    print("Max Time: {0}".format(round(max(move_times), 3)))

    # Winner is the non-active player.
    return 1 - active_player


# This method generates a binomial random graph with 2k vertices
# having probability p of an edge between each pair of vertices.
def BinomialRandomGraph(k, p):
    v = {Vertex(i) for i in range(2 * k)}
    e = {Edge(a, b) for (a, b) in itertools.combinations(v, 2) if random.random() < p}
    return Graph(v, e)


# This method creates and plays a number of random graphs using both passed in players.
def PlayBenchmark(p1, p2, iters):
    global gui_enabled
    gui_enabled = True
    graphs = (
        BinomialRandomGraph(random.randint(2, 20), random.random())
        # BinomialRandomGraph(2, 0.5)
        for _ in range(iters)
    )
    wins = [0, 0]
    instaLosses = 0
    start_time = time.time()
    print("Opp Delta\tV and E Length\tTime For Game")
    for graph in graphs:
        p2_wins = wins[1]
        wins = PlayGame(graph, p1, p2, wins, p2_wins)
        if len(graph.E) == 0 or\
           len(graph.E) == len(graph.V) * (len(graph.V) - 1) / 2:
            instaLosses += 1
        # if wins[1] - p2_wins == 2:
        #     gui_enabled = True
        #     PlayGame(graph, p1, p2, wins, p2_wins)
        #     gui_enabled = False
    print("Average Time: {0}".format(round((time.time() - start_time) / iters, 3)))
    print("Insta Losses: {0}".format(instaLosses))
    return wins

def PlayGame(graph, p1, p2, wins, p2_wins):
    g1 = copy.deepcopy(graph)
    g2 = copy.deepcopy(graph)
    t0 = time.time()
    # Each player gets a chance to go first on each graph.
    if gui_enabled:
        gui.NewGame(g1, 0)
    winner_a = PlayGraph(p1, p2, g1)
    wins[winner_a] += 1
    # print("s")
    if gui_enabled:
        gui.NewGame(g2, 1)
    winner_b = PlayGraph(p2, p1, g2)
    wins[1-winner_b] += 1
    windiff = wins[1] - p2_wins
    if windiff == 0:
        windiff = "-"
    elif windiff == 2:
        windiff = "F"
    print("{0}\t\t{1}, {2}\t\t{3}".format(windiff, len(graph.V), len(graph.E), round(time.time() - t0, 3)))
    return wins

# This is a player that plays a legal move at random.
class RandomPlayer:
    # These are "static methdods" - note there's no "self" parameter here.
    # These methods are defined on the blueprint/class definition rather than
    # any particular instance.
    def ChooseVertexToColor(graph, active_player):
        return random.choice([v for v in graph.V if v.color == -1])

    def ChooseVertexToRemove(graph, active_player):
        return random.choice([v for v in graph.V if v.color == active_player])


if __name__ == "__main__":
    # NOTE: we are not creating INSTANCES of these classes, we're defining the players
    # as the class itself. This lets us call the static methods.
    p1 = percolator.PercolationPlayer
    p2 = RandomPlayer
    iters = 200
    wins = PlayBenchmark(p1, p2, iters)
    print(wins)
    print(
        "Player 1: {0} Player 2: {1}".format(
            1.0 * wins[0] / sum(wins), 1.0 * wins[1] / sum(wins)
        )
    )