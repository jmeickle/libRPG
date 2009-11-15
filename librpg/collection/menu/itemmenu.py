from librpg.menu import Menu, Label, Cursor, Panel, Div


class ExitLabel(Label):

    def __init__(self, theme=None):
        Label.__init__(self, 'Exit', theme=theme)

    def activate(self):
        self.menu.close()


class ItemMenu(Menu):

    def __init__(self, inventory, width, height, x=0, y=0, theme=None, bg=None,
                 mouse_control=Menu.MOUSE_LOOSE):
        self.inventory = inventory
        Menu.__init__(self, width, height, x, y, theme, bg, mouse_control)

        self.exit_label = ExitLabel(theme)
        self.add_widget(self.exit_label, (20, 12))

        self.build_inventory()
        cursor = Cursor()
        cursor.bind(self)

    def build_inventory(self):
        self.inventory_panel = Div(self.width, self.height - 40)
        self.add_widget(self.inventory_panel, (0, 40))

        d = self.inventory.get_items_with_amounts()
        for i, pair in enumerate(d.iteritems()):
            item, qt = pair
            s = '%s x%d' % (item.name, qt)
            label = Label(s)
            self.inventory_panel.add_widget(label, (20, 10 + 25 * i))
