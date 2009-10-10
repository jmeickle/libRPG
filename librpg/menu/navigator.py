import math

from librpg.locals import *

class WidgetNavigator(object):

    def find(self, widget, direction):
        """
        *Abstract.*

        Return the widget reached when going towards *direction* from *widget*.

        Return None if there is no other widget in that direction.
        """
        raise NotImplementedError, 'WidgetNavigator.find() is abstract'

    def enter_div(self, div, direction):
        """
        *Abstract.*

        Return the widget reached when a *div* is entered towards *direction*.

        Return None if the *div* should be skipped.
        """
        raise NotImplementedError, 'WidgetNavigator.enter_div() is abstract'


class DistanceNavigator(WidgetNavigator):

    MAX_DIST = 999999

    def find(self, widget, direction):
        #print '-' * 60
        #print 'find(%s, %d)' % (widget, direction)
        if widget.parent is None:
            return None

        width = widget.menu.width
        height = widget.menu.height

        best = None, DistanceNavigator.MAX_DIST
        for bound_widget in widget.menu.all_widgets:
            if (not bound_widget.is_div()
                and bound_widget.focusable
                and bound_widget is not widget):
                dist = self.calc_distance(widget.get_center(),
                                          bound_widget.get_center(),
                                          direction,
                                          width,
                                          height)
                #print 'comparing to %s = dist %d' % (bound_widget, dist)
                if dist < best[1]:
                    best = bound_widget, dist
        return best[0]

    def calc_distance(self, start, end, direction, width, height):
        raise NotImplementedError, 'DistanceNavigator.calc_distance() is abstract'

    def inside_angle(self, dy, dx, direction):
        if direction == UP:
            return dx <= dy
        elif direction == DOWN:
            return dx <= dy
        elif direction == RIGHT:
            return dy <= dx
        elif direction == LEFT:
            return dy <= dx

    def modulus_distance(self, start, end, n, direction=None):
        """
        Calculate the distance from start to end in a modulus n space.
        """
        if direction is None:
            r = abs(end - start)
            if r > n / 2:
                return n - r
            else:
                return r
        else:
            if direction == RIGHT or direction == DOWN:
                if end < start:
                    return n + end - start
                else:
                    return end - start
            else:
                if end < start:
                    return start - end
                else:
                    return n + start - end


class EuclidianNavigator(DistanceNavigator):

    def calc_distance(self, start, end, direction, width, height):
        if direction == UP:
            dy = self.modulus_distance(start[1], end[1], height, direction)
            dx = self.modulus_distance(start[0], end[0], width)
        elif direction == DOWN:
            dy = self.modulus_distance(start[1], end[1], height, direction)
            dx = self.modulus_distance(start[0], end[0], width)
        elif direction == RIGHT:
            dx = self.modulus_distance(start[0], end[0], width, direction)
            dy = self.modulus_distance(start[1], end[1], height)
        elif direction == LEFT:
            dx = self.modulus_distance(start[0], end[0], width, direction)
            dy = self.modulus_distance(start[1], end[1], height)
        #print 'dx %d, dy %d' % (dx, dy)
        if not self.inside_angle(dy, dx, direction):
            return DistanceNavigator.MAX_DIST
        else:
            return math.sqrt(dx ** 2 + dy ** 2)


class WidgetGateway(object):

    def __init__(self, widget, up=None, right=None, down=None, left=None):
        self.widget = widget
        self.up = up
        self.right = right
        self.down = down
        self.left = left

    def build_map(self):
        self.direction_map = {UP: self.up,
                              RIGHT: self.right,
                              DOWN: self.down,
                              LEFT: self.left}
        #print 'MAP %s %s' % (self.widget, self.direction_map)

    def crystallize(self, widget_navigator):
        self.up = widget_navigator.find(self.widget, UP)
        self.right = widget_navigator.find(self.widget, RIGHT)
        self.down = widget_navigator.find(self.widget, DOWN)
        self.left = widget_navigator.find(self.widget, LEFT)
        self.widget.crystallized = True
        self.build_map()

    def step(self, direction, widget_navigator=None):
        if self.widget.crystallized:
            target = self.direction_map.get(direction, None)
        else:
            assert widget_navigator is not None, 'If WidgetGateway is not '\
                   'crystallized, widget_navigator must be specified'
            target = widget_navigator.find(self.widget, direction)
        return target
