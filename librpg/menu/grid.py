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

    def add_lines(self, number_of_lines=1):
        old_height = self.height_in_cells
        self.height_in_cells += number_of_lines
        self.cells.resize(self.width_in_cells, self.height_in_cells)

        for y in xrange(old_height, self.height_in_cells):
            for x in xrange(self.width_in_cells):
                div = Div(self.cell_width, self.cell_height, focusable=False,
                          theme=self.theme)
                pos = (x * self.cell_width, y * self.cell_height)
                self.cells[x, y] = div
                self.add_widget(div, pos)

    def add_columns(self, number_of_columns=1):
        old_width = self.width_in_cells
        self.width_in_cells += number_of_columns
        self.cells.resize(self.width_in_cells, self.height_in_cells)

        for y in xrange(self.height_in_cells):
            for x in xrange(old_width, self.width_in_cells):
                div = Div(self.cell_width, self.cell_height, focusable=False,
                          theme=self.theme)
                pos = (x * self.cell_width, y * self.cell_height)
                self.cells[x, y] = div
                self.add_widget(div, pos)

    def remove_lines(self, number_of_lines=1):
        if self.height_in_cells <= number_of_lines:
            raise IndexError('Cannot remove %d lines from a Grid with %d '
                             'lines' % (number_of_lines, self.height_in_cells))

        old_height = self.height_in_cells
        self.height_in_cells -= number_of_lines

        for y in xrange(self.height_in_cells, old_height):
            for x in xrange(self.width_in_cells):
                self.remove_widget(self.cells[x, y])

        self.cells.resize(self.width_in_cells, self.height_in_cells)

    def remove_columns(self, number_of_columns=1):
        raise IndexError('Cannot remove %d columns from a Grid with %d '\
                         'columns' % (number_of_columns, self.width_in_cells))
        old_width = self.width_in_cells
        self.width_in_cells -= number_of_columns

        for y in xrange(self.height_in_cells):
            for x in xrange(self.width_in_cells, old_width):
                self.remove_widget(self.cells[x, y])

        self.cells.resize(self.width_in_cells, self.height_in_cells)


class HorizontalGrid(Grid):

    def __init__(self, width, height, width_in_cells, visible=False,
                 focusable=False, theme=None):
        Grid.__init__(self, width, height, width_in_cells, 1, visible,
                      focusable, theme)

    def __getitem__(self, x):
        return self.cells[x, 0]

    def add_lines(self, number_of_lines=1):
        raise Exception('HorizontalGrid cannot have more than 1 line')


class VerticalGrid(Grid):

    def __init__(self, width, height, height_in_cells, visible=False,
                 focusable=False, theme=None):
        Grid.__init__(self, width, height, 1, height_in_cells, visible,
                      focusable, theme)

    def __getitem__(self, y):
        return self.cells[0, y]

    def add_columns(self, number_of_columns=1):
        raise Exception('VerticalGrid cannot have more than 1 column')
