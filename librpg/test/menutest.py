import librpg
from librpg.menu import MenuController, Menu, Panel, Label, ArrowCursor
from librpg.context import get_context_stack

class TestMenu(Menu):

    def __init__(self):
        Menu.__init__(self, 400, 300)
        self.panel = Panel(200, 150)
        self.add_widget(self.panel, (40, 80))
        
        menu_label = Label('Menu')
        self.add_widget(menu_label, (120, 20))
        
        first_panel_label = Label('Panel0')
        self.panel.add_widget(first_panel_label, (40, 40))
        self.panel.add_widget(Label('Panel1'), (120, 40))
        self.panel.add_widget(Label('Panel2'), (40, 80))
        self.panel.add_widget(Label('Panel3'), (120, 80))

        self.side_panel = Panel(110, 220)
        self.add_widget(self.side_panel, (260, 40))
        
        for i in range(6):
            label = Label('SidePanel%d' % i)
            pos = (20, 20 + 30 * i)
            self.side_panel.add_widget(label, pos)

        #self.crystallize()

        # Add cursor
        cursor = ArrowCursor()
        cursor.bind(self, first_panel_label)


def main():
    librpg.init()

    c = MenuController(TestMenu())
    get_context_stack().stack_context(c)
    get_context_stack().gameloop()

if __name__ == '__main__':
    main()

