import pygame
import math
import random

class GUI:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode(size=(800,800))
        pygame.display.set_caption("Percolation Game GUI")
    
    def NewGame(self, graph, player):
        self.win.fill((0, 0, 0))
        c = player * 120 + 120
        color = (c, c, c)
        pygame.draw.circle(self.win, (255, 255, 255), (34, 34), 24)
        pygame.draw.circle(self.win, color, (34, 34), 20)
        self.coord_dict = {}
        num_vertices = len(graph.V)
        for v in graph.V:
            x = 400 + 300 * math.cos(math.pi * (0.5 - v.index / num_vertices * 2))
            y = 400 + 300 * math.sin(math.pi * (0.5 - v.index / num_vertices * 2))
            self.coord_dict.update({v: (x,y)})
        triangle = [(742, 10), (742, 58), (790, 34)]
        pygame.draw.polygon(self.win, (255, 255, 255), triangle)

    def DrawGraph(self, graph, player):
        self.win.fill((0, 0, 0), pygame.Rect(76, 76, 648, 648))
        c = player * 120 + 120
        color = (c, c, c)
        pygame.draw.circle(self.win, (255, 255, 255), (92, 34), 24)
        pygame.draw.circle(self.win, color, (92, 34), 20)
        for e in graph.E:
            pygame.draw.aaline(self.win, (255, 255, 255, 255), self.coord_dict[e.a], self.coord_dict[e.b])
        for v in graph.V:
            c = v.color * 120 + 120
            color = (c, c, c)
            pygame.draw.circle(self.win, (255, 255, 255), self.coord_dict[v], 24)
            pygame.draw.circle(self.win, color, self.coord_dict[v], 20)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.Pause()
        if len(graph.V) < 8:
            pygame.time.delay(2000)
    
    def Pause(self):
        paused = True
        triangle = [(742, 10), (742, 58), (790, 34)]
        pygame.draw.rect(self.win, (255, 255, 255), pygame.Rect(742, 10, 48, 48))
        pygame.display.update()
        while paused:
            pygame.time.delay(100)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.draw.rect(self.win, (0, 0, 0), pygame.Rect(742, 10, 48, 48))
                        pygame.draw.polygon(self.win, (255, 255, 255), triangle)
                        pygame.display.update()
                        paused = False

class PercolationPlayer:
    gui = GUI()

    @staticmethod
    def ChooseVertexToColor(graph, player):
        if all(v.color == -1 for v in graph.V):
            PercolationPlayer.gui.NewGame(graph)
        PercolationPlayer.gui.DrawGraph(graph)
        return random.choice([v for v in graph.V if v.color == -1])

    @staticmethod
    def ChooseVertexToRemove(graph, player):
        PercolationPlayer.gui.DrawGraph(graph)
        return random.choice([v for v in graph.V if v.color == player])