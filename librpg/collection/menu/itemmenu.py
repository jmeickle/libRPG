from librpg.menu import Menu, Label, Cursor, Panel, VerticalScrollArea
from librpg.color import TRANSPARENT


class ExitLabel(Label):

    def __init__(self):
        Label.__init__(self, 'Exit')

    def activate(self):
        self.menu.close()
        return True


class ItemLabel(Label):

    def __init__(self, item, quantity, inventory):
        self.item = item
        self.quantity = quantity
        self.inventory = inventory
        s = self.create_string()
        Label.__init__(self, s)

    def activate(self):
        dialog = self.menu.create_action_dialog(self)
        dialog.sync_open()
        return True

    def refresh(self):
        self.quantity = self.inventory.get_amount(self.item)
        self.text = self.create_string()

    def create_string(self):
        return '%s x%d' % (self.item.name, self.quantity)


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

        self.config_action_dialog(100, 60, TRANSPARENT)

    def build_inventory(self):
        inv = self.inventory

        self.inventory_panel = VerticalScrollArea(self.width - 20,
                                                  self.height - 50,
                                                  24)
        self.add_widget(self.inventory_panel, (10, 40))

        ordered = inv.get_ordered_list()
        amounts = inv.get_items_with_amounts()

        pairs = [(item, amounts[item]) for item in ordered]
        for _, pair in enumerate(pairs):
            item, qt = pair
            label = ItemLabel(item, qt, inv)
            line = self.inventory_panel.add_line()
            self.inventory_panel[line].add_widget(label, (20, 10))

    def config_action_dialog(self, width=None, height=None, bg=None):
        if width is not None:
            self.action_dialog_width = width
        if height is not None:
            self.action_dialog_height = height
        self.action_dialog_bg = bg

    def create_action_dialog(self, item_label):
        x, y = item_label.get_menu_position()
        x += item_label.width + 10
        dialog = ActionDialog(self, item_label.item, item_label.quantity,
                              item_label,
                              self.action_dialog_width,
                              self.action_dialog_height, x, y,
                              theme=self.theme,
                              bg=self.action_dialog_bg)
        return dialog

    def remove_line(self, item):
        for i in xrange(len(self.inventory_panel)):
            if self.inventory_panel[i].get_contents()[0].item == item:
                self.inventory_panel.remove_line(i)
                break


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
            self.menu.item_menu.remove_line(self.item)
            self.menu.close()
        else:
            self.item_label.refresh()
        return True


class ActionDialog(Menu):

    def __init__(self, item_menu, item, quantity, item_label, width, height,
                 x=0, y=0, theme=None, bg=TRANSPARENT,
                 mouse_control=Menu.MOUSE_LOOSE):
        Menu.__init__(self, width, height, x, y, theme, bg, mouse_control)
        self.item_menu = item_menu

        self.item = item
        self.quantity = quantity

        self.panel = Panel(width, height)
        self.add_widget(self.panel, (0, 0))
        
        self.use_label = UseLabel(self.item, self.item_menu.inventory, None,
                                  item_label)
        self.panel.add_widget(self.use_label, (20, 12))

        self.exit_label = ExitLabel()
        self.panel.add_widget(self.exit_label, (20, 36))

        cursor = Cursor()
        cursor.bind(self)
