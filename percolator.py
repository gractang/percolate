# this is in percolate, my own repo.
import random
import sys
"""
You'll want to implement a smarter decision logic. This is skeleton code that you should copy and replace in your repository.
"""
class PercolationPlayer:
    def Neighbors(graph, node):
        adjacents = set()
        for edge in graph.E:
            if edge.a == node:
                adjacents.add(edge.b)
            elif edge.b == node:
                adjacents.add(edge.a)
        return adjacents

    def IncidentEdges(graph, node):
        return [e for e in graph.E if (e.a == node or e.b == node)]

    def EvaluateNode(graph, player, node):
        score = 0
        neighbors = PercolationPlayer.Neighbors(graph, node)
        num_neighbors = 0
        for neighbor in neighbors:
            n_degree = len(PercolationPlayer.IncidentEdges(graph, neighbor))
            if n_degree == 1:
                if neighbor.color == player:
                    score -= 10
                else:
                    score += 10

            # num connected that are of the other color
            if neighbor.color != player:
                score += 1

            score -= 1
        return score

    def EvalColor(graph, player, node):
        score = 0
        score += len(PercolationPlayer.IncidentEdges(graph, node))
        return score

    # recursive method that returns 1 if the state is good and 0 if the state is bad
    def Eval(graph, player):
        num_nodes = len(graph.v)
        # presuming it is player's turn
        if num_nodes == 0:
            return 0
        if num_nodes == 2:
            for node in graph.v:
                if node.color == player:
                    return 1
            return 0
        else:
            for node in graph.v:
                if node.color == player:
                    new_g = Remove(graph, node)

                    # is not good
                    if not Eval(new_g, node):
                        return 0
            return 1

    def ChooseVertexToColor(graph, player):
        highscore = -sys.maxsize - 1
        v_to_c = None
        for v in graph.V:
            if v.color == -1:
                vscore = PercolationPlayer.EvalColor(graph, player, v)
                if vscore > highscore:
                    v_to_c = v
                    highscore = vscore
        return v_to_c

    def ChooseVertexToRemove(graph, player):
        #supposely min value
        highscore = -sys.maxsize - 1
        v_to_rm = None
        for v in graph.V:
            if v.color == player:
                vscore = PercolationPlayer.EvaluateNode(graph, player, v)
                if vscore > highscore:
                    v_to_rm = v
                    highscore = vscore
        return v_to_rm
        # return random.choice([v for v in graph.V if v.color == player])
