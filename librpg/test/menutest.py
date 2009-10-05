import librpg
from librpg.menu import MenuController, Menu, Panel, Div
from librpg.context import get_context_stack

class TestMenu(Menu):

    def __init__(self):
        Menu.__init__(self, 400, 300)
        self.add_widget(Panel(100, 100), (10, 10))


def main():
    librpg.init()

    c = MenuController(TestMenu())
    get_context_stack().stack_context(c)
    get_context_stack().gameloop()

if __name__ == '__main__':
    main()

