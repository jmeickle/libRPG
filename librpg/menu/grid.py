from librpg.menu.div import Div
from librpg.util import Matrix

class Grid(Div):

    def __init__(self, width, height, width_in_cells, height_in_cells,
                 visible=False, focusable=False, theme=None):
        Div.__init__(self, width, height, focusable, theme)
        self.visible = visible
        self.width_in_cells = width_in_cells
        self.height_in_cells = height_in_cells
        self.cell_width = self.width / self.width_in_cells
        self.cell_height = self.height / self.height_in_cells

        self.cells = Matrix(width_in_cells, height_in_cells)
        for y in xrange(height_in_cells):
            for x in xrange(width_in_cells):
                div = Div(self.cell_width, self.cell_height, focusable=False,
                          theme=self.theme)
                pos = (x * self.cell_width, y * self.cell_height)
                self.cells[x, y] = div
                self.add_widget(div, pos)

    def __getitem__(self, pos):
        return self.cells[pos]


class HorizontalGrid(Grid):

    def __init__(self, width, height, width_in_cells, visible=False,
                 focusable=False, theme=None):
        Grid.__init__(self, width, height, width_in_cells, 1, visible,
                      focusable, theme)

    def __getitem__(self, x):
        return self.cells[x, 0]


class VerticalGrid(Grid):

    def __init__(self, width, height, height_in_cells, visible=False,
                 focusable=False, theme=None):
        Grid.__init__(self, width, height, 1, height_in_cells, visible,
                      focusable, theme)

    def __getitem__(self, y):
        return self.cells[0, y]
