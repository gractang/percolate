# this is in percolation.
import random
import itertools
import copy
import sys
import traceback

import time
import signal
import errno
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

    # Gets a vertex with given index if it exists, else return None.
    def GetVertex(graph, i):
        for v in graph.V:
            if v.index == i:
                return v
        return None

    # Removes the given vertex v from the graph, as well as the edges attached to it.
    # Removes all isolated vertices from the graph as well.
    def Percolate(graph, v):
        # Get attached edges to this vertex, remove them.
        for e in PercolationPlayer.IncidentEdges(graph, v):
            graph.E.remove(e)
        # Remove this vertex.
        graph.V.remove(v)
        # Remove all isolated vertices.
        to_remove = {u for u in graph.V if len(PercolationPlayer.IncidentEdges(graph, u)) == 0}
        graph.V.difference_update(to_remove)

    def Minimax(player, graph, maxTurn): 
        valids = [v for v in graph.V if v.color == player]
        if not valids:
            return (-42, None) if maxTurn else (42, None)
        
        if maxTurn:
            bestVal = -sys.maxsize - 1

            # bestNode
            medmond = None
            for v in valids:
                new_graph = copy.deepcopy(graph)
                PercolationPlayer.Percolate(new_graph, PercolationPlayer.GetVertex(new_graph, v.index))

                # vert is actually useless but i can't be bothered
                value, vert = PercolationPlayer.Minimax(1 - player, new_graph, not maxTurn)

                # update medmond + bestVal
                if bestVal <= value:
                    bestVal = value
                    medmond = v

            return (bestVal, medmond)

        else:
            # min now
            bestVal = sys.maxsize 

            # bestNode, but min
            ratthew = None
            for v in valids:
                new_graph = copy.deepcopy(graph)
                PercolationPlayer.Percolate(new_graph, PercolationPlayer.GetVertex(new_graph, v.index))
                value, vert = PercolationPlayer.Minimax(1 - player, new_graph, not maxTurn)

                # update medmond + bestVal
                if bestVal >= value:
                    bestVal = value
                    ratthew = v

            return (bestVal, ratthew)

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
        neighbors = PercolationPlayer.Neighbors(graph, node)
        for neighbor in neighbors:
            if neighbor.color == player:
                score += 3
            elif neighbor.color == 1 - player:
                score += 1
            else:
                score += 2
        score += len(PercolationPlayer.IncidentEdges(graph, node))
        return score


    def ChooseVertexToColor(graph, player):
        highscore = -sys.maxsize - 1
        v_to_c = None
        for v in graph.V:
            if v.color == -1:
                vscore = PercolationPlayer.EvalColor(graph, player, v)
                if vscore > highscore:
                    v_to_c = v
                    highscore = vscore
        return v_to_c if v_to_c else random.choice([v for v in graph.V if v.color == -1])

    def ChooseVertexToRemove(graph, player):
        #supposely min value
        num_nodes = len(graph.V)
        if num_nodes < 10:
            value, vertex = PercolationPlayer.Minimax(player, graph, False)
            # print(vertex)
            # print(graph)

            return PercolationPlayer.Minimax(player, graph, False)[2-1]

        highscore = -sys.maxsize - 1
        v_to_rm = None
        for v in graph.V:
            if v.color == player:
                vscore = PercolationPlayer.EvaluateNode(graph, player, v)
                if vscore > highscore:
                    v_to_rm = v
                    highscore = vscore
        return v_to_rm if v_to_rm else random.choice([v for v in graph.V if v.color == player])
