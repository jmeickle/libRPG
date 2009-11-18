from librpg.menu import Menu, Label, Cursor, Panel, Div, VerticalScrollArea


class ExitLabel(Label):

    def __init__(self):
        Label.__init__(self, 'Exit')

    def activate(self):
        self.menu.close()
        return True


class ItemLabel(Label):

    def __init__(self, item, quantity, inventory):
        s = '%s x%d' % (item.name, quantity)
        Label.__init__(self, s)
        self.item = item
        self.quantity = quantity
        self.inventory = inventory

    def activate(self):
        dialog = self.menu.create_action_dialog(self)
        dialog.open()
        return True

    def refresh(self):
        quantity = self.inventory.get_amount(self.item)
        self.text = '%s x%d' % (self.item.name, quantity)


class ItemMenu(Menu):

    def __init__(self, inventory, width, height, x=0, y=0, theme=None, bg=None,
                 mouse_control=Menu.MOUSE_LOOSE):
        self.inventory = inventory
        Menu.__init__(self, width, height, x, y, theme, bg, mouse_control)

        self.exit_label = ExitLabel()
        self.add_widget(self.exit_label, (20, 12))

        self.inventory_panel = None
        self.build_inventory()
        cursor = Cursor()
        cursor.bind(self)

        self.config_action_dialog(100, 60)

    def build_inventory(self):
        if self.inventory_panel is not None:
            self.remove_widget(self.inventory_panel)
        self.inventory_panel = VerticalScrollArea(self.width, self.height - 40)
        self.add_widget(self.inventory_panel, (0, 40))

        d = self.inventory.get_items_with_amounts()
        for i, pair in enumerate(d.iteritems()):
            item, qt = pair
            label = ItemLabel(item, qt, self.inventory)
            self.inventory_panel.add_widget(label, (20, 10 + 25 * i))

    def config_action_dialog(self, width=None, height=None, bg=None):
        if width is not None:
            self.action_dialog_width = width
        if height is not None:
            self.action_dialog_height = height
        if bg is not None:
            self.action_dialog_bg = bg

    def create_action_dialog(self, item_label):
        x, y = item_label.get_menu_position()
        x += item_label.width + 10
        dialog = ActionDialog(self, item_label.item, item_label.quantity,
                              item_label,
                              self.action_dialog_width,
                              self.action_dialog_height, x, y,
                              bg=self.action_dialog_bg)
        return dialog

    def refresh(self):
        self.build_inventory()


# Action Dialog

class UseLabel(Label):

    def __init__(self, item, inv, party, item_label):
        Label.__init__(self, 'Use')
        self.item = item
        self.inv = inv
        self.party = party
        self.item_label = item_label

    def activate(self):
        print 'Used %s' % self.item.name
        self.inv.remove_item(self.item)
        if not self.inv.contains(self.item):
            self.menu.item_menu.refresh()
            self.menu.close()
        else:
            self.item_label.refresh()
        return True


class ActionDialog(Menu):

    def __init__(self, item_menu, item, quantity, item_label, width, height,
                 x=0, y=0, theme=None, bg=None,
                 mouse_control=Menu.MOUSE_LOOSE):
        Menu.__init__(self, width, height, x, y, theme, bg, mouse_control)
        self.item_menu = item_menu

        self.item = item
        self.quantity = quantity

        self.use_label = UseLabel(self.item, self.item_menu.inventory, None,
                                  item_label)
        self.add_widget(self.use_label, (20, 12))

        self.exit_label = ExitLabel()
        self.add_widget(self.exit_label, (20, 36))

        cursor = Cursor()
        cursor.bind(self)
