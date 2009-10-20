import heapq
from pygame.locals import *

class StarA(object):
    def __init__(self, mapmodel, start, goal):

        came_from = {}

        self.start = start
        self.goal = goal
        self.closed = []
        self.open = [(self.h(start), start), ]

        while len(self.open) > 0:
            least = heapq.heappop(self.open)
            prediction, value, x = least

            if x == goal:
                def follow(n):
                    if n == start:
                        return [start,]
                    else:
                        return follow(came_from[n])+[n,]

                return follow(least)

            for f, y in zip([UP,DOWN,LEFT,RIGHT],
                         [x.up(), x.down(), x.left(),x.right()]):
                
                if mapmodel.can_move(x, y, f):
                    next = (value+1+self.h(y), value+1, y)
                    came_from[next] = least
                    heapq.heappush(self.open, least)
                    
    def h(self, pos):
        """
        Manhattan distance
        """

        return abs(pos.x-goal.x)+abs(pos.y-goal.y)
