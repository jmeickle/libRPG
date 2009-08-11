from librpg.util import Position

class MapArea:

    def __init__(self):
        self.area = []

    # Virtual
    def party_entered(self, party_avatar, position):
        pass

    # Virtual
    def party_moved(self, party_avatar, left_position, entered_position,
                    from_outside):
        pass

    # Virtual
    def party_left(self, party_avatar, position):
        pass


class RectangleArea:

    def __init__(self, top_left, bottom_right):
        self.top = top_left[1]
        self.left = top_left[0]
        self.bottom = bottom_right[1]
        self.right = bottom_right[0]
        self.cur_x = self.left
        self.cur_y = self.top
        
    def __getitem__(self, index):
        if self.cur_y > self.bottom:
            raise IndexError('Finished')
        result = Position(self.cur_x, self.cur_y)
        self.cur_x += 1
        if self.cur_x > self.right:
            self.cur_x = self.left
            self.cur_y += 1
        return result
