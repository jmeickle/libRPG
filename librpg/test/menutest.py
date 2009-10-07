import librpg
from librpg.menu import MenuController, Menu, Panel, Label
from librpg.context import get_context_stack

class TestMenu(Menu):

    def __init__(self):
        Menu.__init__(self, 400, 300)
        self.panel = Panel(100, 120)
        self.add_widget(self.panel, (40, 40))
        self.add_widget(Label('Menu'), (10, 10))
        self.panel.add_widget(Label('Panel'), (10, 10))
        self.crystallize()


def main():
    librpg.init()

    c = MenuController(TestMenu())
    get_context_stack().stack_context(c)
    get_context_stack().gameloop()

if __name__ == '__main__':
    main()

