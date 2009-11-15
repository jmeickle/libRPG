from librpg.menu import Menu, Label, AlignTopRight, Cursor, Panel, AlignCenter


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

        self.master_panel = Panel(width, height, False, theme)
        self.add_widget(self.master_panel, AlignCenter())

        self.exit_label = ExitLabel(theme)
        self.master_panel.add_widget(self.exit_label, AlignTopRight(8))

        cursor = Cursor()
        cursor.bind(self)
