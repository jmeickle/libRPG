from librpg.menu import Div, Label, AlignCenter


class TabGroup(Div):

    def __init__(self, ids, width, height, tab_width=None, tab_height=None, 
                 focusable=False, theme=None, initial_tab=None):
        Div.__init__(self, width, height, focusable, theme)

        # Find ids
        self.ids = ids

        # Setup dimensions
        if tab_width is None:
            self.tab_width = max(30, self.width / 8)
        else:
            self.tab_width = tab_width
        if tab_height is None:
            self.tab_height = min(10, self.height / 2)
        else:
            self.tab_height = tab_height
        self.area_height = self.height - self.tab_height

        # Create areas and tabs
        self.areas = {}
        self.tabs = []
        for i, id in enumerate(self.ids):
            div = Div(self.width, self.area_height, focusable, theme)
            self.areas[id] = div

            tab = Tab(self, self.tab_width, self.tab_height, id)
            self.add_widget(tab, (i * self.tab_width, 0))
            self.tabs.append(tab)

        # Set initial tab area
        self.current = None
        if initial_tab is not None:
            self.focus(initial_tab)
        elif self.areas:
            self.focus(self.ids[0])

    def __getitem__(self, id):
        try:
            return self.areas[id]
        except:
            return self.areas.get(self.ids[id], None)

    def focus(self, id):
        if self.current != id:
            if self.current is not None:
                self.remove_widget(self.current)
            self.add_widget(self[id], (0, self.tab_height))
            self.current = self[id]


class Tab(Div):

    def __init__(self, tab_group, width, height, id, theme=None):
        Div.__init__(self, width, height, False, theme)
        self.label = TabLabel(tab_group, id, theme=self.theme)
        self.add_widget(self.label, AlignCenter())


class TabLabel(Label):

    def __init__(self, tab_group, id, theme=None):
        Label.__init__(self, id, focusable=True, theme=theme)
        self.tab_group = tab_group
        self.id = id

    def activate(self):
        self.tab_group.focus(self.id)
