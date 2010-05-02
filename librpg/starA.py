import heapq
from librpg.locals import UP, DOWN, LEFT, RIGHT


class StarA(object):

    def __init__(self, mapmodel, start, goal):

        self.came_from = {}

        self.mm = mapmodel
        self.start = start
        self.goal = goal
        self.closed = set()
        self.open = [(self.h(start), 0, start, None), ]

    def calculate(self):

        while len(self.open) > 0:

            least = heapq.heappop(self.open)
            prediction, value, x, _ = least

            if x == self.goal:

                def follow(n):
                    _, _, y, f = n
                    if y == self.start:
                        return []
                    else:
                        return follow(self.came_from[n]) + [f, ]

                return follow(least)

            for f, y in zip([UP, DOWN, LEFT, RIGHT],
                            [x.up(), x.down(), x.left(), x.right()]):

                if y not in self.closed and self.mm.can_move(x, y, f):
                    next = (value + 1 + self.h(y), value + 1, y, f)
                    self.came_from[next] = least
                    heapq.heappush(self.open, next)
                    self.closed.add(y)
        return None

    def h(self, pos):
        """
        Manhattan distance
        """

        return abs(pos.x - self.goal.x) + abs(pos.y - self.goal.y)
