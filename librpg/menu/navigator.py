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
        best = None, DistanceNavigator.MAX_DIST
        for other_widget in widget.parent.widgets:
            if other_widget is not widget:
                dist = self.calc_distance(widget.position, other_widget.position, direction)
                if dist < best[1]:
                    best = other_widget, dist
        return best[0]

    def enter_div(self, div, direction):
        pos = (div.width / 2, div.height / 2)
        best = None, DistanceNavigator.MAX_DIST
        for widget in widget.parent.widgets:
            dist = self.calc_distance(pos, widget.position, direction)
            if dist < best[1]:
                best = widget, dist
        return best[0]

    def calc_distance(self, start, end, direction):
        raise NotImplementedError, 'DistanceNavigator.calc_distance() is abstract'

    def inside_angle(self, dy, dx, direction):
        angle = math.atan2(dy, dx)
        if direction == UP:
            if angle < math.pi / 4 or angle > 3 * math.pi / 4:
                return False
        elif direction == RIGHT:
            if abs(angle) > math.pi / 4:
                return False
        elif direction == DOWN:
            if angle > - math.pi / 4 or angle < -3 * math.pi / 4:
                return False
        elif direction == LEFT:
            if abs(angle) < 3 * math.pi / 4:
                return False
        return True


class EuclidianNavigator(DistanceNavigator):

    def calc_distance(self, start, end, direction):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        angle = math.atan2(dy, dx)
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

    def crystallize(self, widget_navigator):
        self.up = widget_navigator.find(self.widget, UP)
        self.right = widget_navigator.find(self.widget, RIGHT)
        self.down = widget_navigator.find(self.widget, DOWN)
        self.left = widget_navigator.find(self.widget, LEFT)

    def div_crystallize(self, widget_navigator):
        self.up = widget_navigator.enter_div(self.widget, UP)
        self.right = widget_navigator.enter_div(self.widget, RIGHT)
        self.down = widget_navigator.enter_div(self.widget, DOWN)
        self.left = widget_navigator.enter_div(self.widget, LEFT)
