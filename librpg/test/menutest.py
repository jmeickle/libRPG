import librpg
from librpg.menu import MenuController, Menu, Panel, Label, HighlightCursor
from librpg.context import get_context_stack

class TestMenu(Menu):

    def __init__(self):
        Menu.__init__(self, 400, 300)
        self.panel = Panel(100, 120)
        self.add_widget(self.panel, (40, 40))
        
        menu_label = Label('Menu')
        self.add_widget(menu_label, (10, 10))
        
        panel_labels = [None] * 4
        panel_labels[0] = Label('Panel0')
        self.panel.add_widget(panel_labels[0], (10, 10))
        panel_labels[1] = Label('Panel1')
        self.panel.add_widget(panel_labels[1], (50, 10))
        panel_labels[2] = Label('Panel2')
        self.panel.add_widget(panel_labels[2], (10, 50))
        panel_labels[3] = Label('Panel3')
        self.panel.add_widget(panel_labels[3], (50, 50))

        self.crystallize()

        cursor = HighlightCursor()
        cursor.bind(self, panel_labels[0])


def main():
    librpg.init()

    c = MenuController(TestMenu())
    get_context_stack().stack_context(c)
    get_context_stack().gameloop()

if __name__ == '__main__':
    main()

