from librpg.menu import (Menu, Label, Cursor, Panel, VerticalScrollArea,
                         ImageWidget)
from librpg.color import TRANSPARENT
from librpg.config import graphics_config
from librpg.menu.div import WidgetGroup


class ExitLabel(Label):

    def __init__(self):
        Label.__init__(self, 'Exit')

    def activate(self):
        self.menu.close()
        return True


class ItemMenu(Menu):

    def __init__(self, inventory, party, width, height, x=0, y=0, theme=None,
                 bg=None, mouse_control=Menu.MOUSE_LOOSE):
        self.inventory = inventory
        self.party = party
        Menu.__init__(self, width, height, x, y, theme, bg, mouse_control)

        self.exit_label = ExitLabel()
        self.add_widget(self.exit_label, (20, 12))

        self.inventory_panel = ItemScrollArea(self.inventory, self.width * 0.5,
                                              self.height - 50,
                                              36, (20, 10))
        self.add_widget(self.inventory_panel, (10, 40))
        
        self.info_panel = ItemInfoPanel(self.width * 0.4, self.height * 0.5)
        inv_space = (self.inventory_panel.position[0]
                           + self.inventory_panel.width)
        spacing = (self.width - inv_space - self.info_panel.width) / 2
        info_x = inv_space + spacing
        info_y = self.height - self.info_panel.height - spacing
        self.add_widget(self.info_panel, (info_x, info_y))
        
        cursor = Cursor()
        cursor.bind(self)

        self.config_action_dialog(100, 60, TRANSPARENT)

    def config_action_dialog(self, width=None, height=None, bg=None):
        if width is not None:
            self.action_dialog_width = width
        if height is not None:
            self.action_dialog_height = height
        self.action_dialog_bg = bg

    def create_action_dialog(self, item_entry):
        x = (self.inventory_panel.get_menu_position()[0]
             + self.inventory_panel.width + 12) 
        y = self.menu.y + 12
        dialog = ActionDialog(self, item_entry.item, item_entry.quantity,
                              item_entry,
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


class ItemScrollArea(VerticalScrollArea):
    
    def __init__(self, inventory, width, height, cell_height,
                 label_pos_inside_cell):
        VerticalScrollArea.__init__(self, width, height, cell_height)
        self.inventory = inventory
        
        ordered = inventory.get_ordered_list()
        BORDER = 12
        for item in ordered:
            group = ItemEntry(width - 10 - 2 * BORDER,
                              self.cell_height - 2 * BORDER,
                              item, inventory,
                              (label_pos_inside_cell[0] - BORDER,
                               label_pos_inside_cell[1] - BORDER))
            line = self.add_line()
            self[line].add_widget(group, (BORDER, BORDER))


class ItemEntry(WidgetGroup):
    
    def __init__(self, width, height, item, inventory, label_pos):
        WidgetGroup.__init__(self, width, height)
        self.item = item
        self.quantity = inventory.get_amount(item)
        self.inventory = inventory
        s = self.create_string()
        self.label = Label(s)
        self.add_widget(self.label, label_pos)

    def activate(self):
        dialog = self.menu.create_action_dialog(self)
        dialog.sync_open()
        return True

    def refresh(self):
        self.quantity = self.inventory.get_amount(self.item)
        self.label.text = self.create_string()

    def create_string(self):
        return '%s x%d' % (self.item.name, self.quantity)


# Action Dialog

class UseLabel(Label):

    def __init__(self, item, inv, party, item_entry):
        Label.__init__(self, 'Use')
        self.item = item
        self.inv = inv
        self.party = party
        self.item_entry = item_entry

    def activate(self):
        print 'Used %s' % self.item.name
        self.item.use(self.party)
        self.inv.remove_item(self.item)
        if not self.inv.contains(self.item):
            self.menu.item_menu.remove_line(self.item)
            self.menu.close()
        else:
            self.item_entry.refresh()
        return True

class TrashLabel(Label):

    def __init__(self, item, inv, item_entry):
        Label.__init__(self, 'Trash')
        self.item = item
        self.inv = inv
        self.item_entry = item_entry

    def activate(self):
        print 'Trashed %s' % self.item.name
        self.inv.remove_item(self.item)
        if not self.inv.contains(self.item):
            self.menu.item_menu.remove_line(self.item)
            self.menu.close()
        else:
            self.item_entry.refresh()
        return True


class ActionDialog(Menu):

    def __init__(self, item_menu, item, quantity, item_entry, width, height,
                 x=0, y=0, theme=None, bg=TRANSPARENT,
                 mouse_control=Menu.MOUSE_LOOSE):
        Menu.__init__(self, width, height, x, y, theme, bg, mouse_control)
        self.item_menu = item_menu

        self.item = item
        self.quantity = quantity

        self.panel = Panel(width, height)
        self.add_widget(self.panel, (0, 0))
        
        if hasattr(item, 'use'):
            self.use_label = UseLabel(self.item, self.item_menu.inventory,
                                      self.item_menu.party, item_entry)
        else:
            self.use_label = TrashLabel(self.item, self.item_menu.inventory, 
                                        item_entry)
        self.panel.add_widget(self.use_label, (20, 12))

        self.exit_label = ExitLabel()
        self.panel.add_widget(self.exit_label, (20, 36))

        cursor = Cursor()
        cursor.bind(self)


class ItemInfoPanel(Panel):

    def __init__(self, width, height):
        Panel.__init__(self, width, height, focusable=False)
        
        self.item_icon = ImageWidget(None, focusable=False)
        x = 10
        y = 10
        self.add_widget(self.item_icon, (x, y))

        self.item_name = Label("", focusable=False)
        x = 10 + graphics_config.item_icon_width + 5
        y = 10 + (graphics_config.item_icon_height - self.item_name.height) / 2
        self.add_widget(self.item_name, (x, y))
        
        self.item_description = Label("", self.width - 20, size=10,
                                      focusable=False)
        x = 10
        y = (10 + max(self.item_name.height, graphics_config.item_icon_height)
             + 10)
        self.add_widget(self.item_description, (x, y))

    def update(self):
        if hasattr(self.menu.cursor.widget, 'item'):
            item = self.menu.cursor.widget.item
            name = item.name
            description = item.get_description()
            icon = item.get_icon()
        else:
            name = ''
            description = ''
            icon = None
            
        if self.item_name.text != name:
            self.item_name.text = name
            self.item_description.text = description
            if icon is not None:
                self.item_icon.surf = icon.get_surface()
            else:
                self.item_icon.surf = None
