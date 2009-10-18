from librpg.menu.div import Div

class Grid(Div):

    def __init__(self, width, height, width_in_cells, height_in_cells,
                 visible=False, focusable=False, theme=None):
        Div.__init__(self, width, height, focusable, theme)
        self.visible = visible
        self.width_in_cells = width_in_cells
        self.height_in_cells = height_in_cells
        self.cell_width = self.width / self.width_in_cells
        self.cell_height = self.height / self.height_in_cells

        self.cells = []
        for i in xrange(height_in_cells):
            line = []
            for j in xrange(width_in_cells):
                div = Div(self.cell_width, self.cell_height, focusable=False,
                          theme=self.theme)
                pos = (j * self.cell_width, i * self.cell_height)
                line.append(div)
                self.add_widget(div, pos)
            self.cells.append(line)

    def __getitem__(self, pos):
        x, y = pos
        return self.cells[y][x]


class HorizontalGrid(Grid):

    def __init__(self, width, height, width_in_cells, visible=False,
                 focusable=False, theme=None):
        Grid.__init__(self, width, height, width_in_cells, 1, visible,
                      focusable, theme)

    def __getitem__(self, x):
        return self.cells[0][x]


class VerticalGrid(Grid):

    def __init__(self, width, height, height_in_cells, visible=False,
                 focusable=False, theme=None):
        Grid.__init__(self, width, height, 1, height_in_cells, visible,
                      focusable, theme)

    def __getitem__(self, y):
        return self.cells[y][0]
