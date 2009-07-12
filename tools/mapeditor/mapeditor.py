#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gobject
import gtk
import gtk.glade
import map
import tools
import config
import numpy

import pygame
from pygame.locals import *
import tools

from kiwi import tasklet
import cPickle

import tile

#def surface2pixbuf(surface):
    #pygame.display.init()
    #surface = tmpsurface.convert(8)
    #pygame.display.quit()
    #surface = tmpsurface
    #    pygame.surfarray.use_arraytype('Numeric')
    #    array = pygame.surfarray.array3d(surface)
    #print array.typecode(),array.shape,surface.get_bitsize()
    #    return gtk.gdk.pixbuf_new_from_array(array, gtk.gdk.COLORSPACE_RGB, 8).rotate_simple(gtk.gdk.PIXBUF_ROTATE_CLOCKWISE)

def tilenumber(iTS,iTile):
    return (iTS << 4) | (iTile << 12) | 0xF
    
class mapeditor(object):
    def __init__(self):
        
        self.gui = gtk.glade.XML('gui/gui.glade')
        self.window=self.gui.get_widget('winmain')
        #self.window.maximize()
        
        self.statusbar=self.gui.get_widget('status')
        
        dic = {"gtk_main_quit" : gtk.main_quit}
        self.gui.signal_autoconnect(dic)	
        self.gui.signal_autoconnect(self)		
        self.window.show_all()		
        
        self.daMap = self.gui.get_widget('daMap')
        
        self.tvTiles = self.gui.get_widget( "tvTiles" )
        #self.tvTilesModel = gtk.ListStore(gtk.gdk.Pixbuf, str)
        self.tvTilesModel = gtk.TreeStore(gtk.gdk.Pixbuf, str)
        self.tvTiles.set_model(self.tvTilesModel)
        
        self.menuLayer = self.gui.get_widget('menuLayer')
        self.layers = []
        
        #renderer = gtk.CellRendererPixbuf()
        #column = gtk.TreeViewColumn('Tiles', renderer, pixbuf=0)
        #self.tvTiles.append_column(column)
        
        #PYGTK faq trick 13.6 - O.o
        column = gtk.TreeViewColumn()
        column.set_title('Tiles')
        self.tvTiles.append_column(column)
        
        renderer = gtk.CellRendererPixbuf()
        column.pack_start(renderer, expand=False)
        column.add_attribute(renderer, 'pixbuf', 0)
        
        renderer = gtk.CellRendererText()
        column.pack_start(renderer, expand=True)
        column.add_attribute(renderer, 'text', 1)
        
        self.miNew   = self.gui.get_widget( "miNew" )
        self.miOpen  = self.gui.get_widget( "miOpen" )
        self.miSave  = self.gui.get_widget( "miSave" )
        self.miSaveAs= self.gui.get_widget( "miSaveAs" )
        self.miQuit  = self.gui.get_widget( "miQuit" )
        
        self.miCut   = self.gui.get_widget( "miSave" )
        self.miCopy  = self.gui.get_widget( "miCopy" )
        self.miPaste = self.gui.get_widget( "miPaste" )
        self.miClear = self.gui.get_widget( "miClear" )
        
        self.miAbout = self.gui.get_widget( "miAbout" )
        
        self.tbFill    = self.gui.get_widget( "tbFill" )
        self.tbReplace = self.gui.get_widget( "tbReplace" )
        
        self.tbCollision = self.gui.get_widget( "tbCollision" )
        self.tbScript = self.gui.get_widget( "tbScript" )
        
        #--- events ---
        
        self.cursor = {}
        self.pixtiles = []
        self.select = 0
        self.layer = 0
        
        self.map = map.MapData()
        
        gtk.main()

    def on_tvTiles_cursor_changed(self, *args):
        (_, i) = self.tvTiles.get_selection().get_selected()
        if i:
            try:
                (pixbuf,iTS,iTile) = self.cursor[self.tvTilesModel.get_string_from_iter(i)]
                self.select = tilenumber(iTS,iTile)
            except KeyError:
                pass
    
    def on_daMap_realize(self, widget):
        self.daMapWindow = widget.window
        self.gc = self.daMapWindow.new_gc()
        
    def on_daMap_expose_event(self, *args):
        map = self.map
        if map:
            for l in xrange(map.nlayers):
                for i in xrange(map.h):
                    for j in xrange(map.w):
                        v = map.tiles[l][i][j]
                        if v > 0:
                            self.daMapWindow.draw_pixbuf(self.gc, self.pixtiles[(v&0x00000FF0) >> 4][(v&0xFFFFF000) >> 12], 0, 0, j*map.tw, i*map.th)
            for i in xrange(map.h):
                for j in xrange(map.w):
                    self.daMapWindow.draw_rectangle(self.gc, False, j*map.tw, i*map.th, map.tw, map.th)
                    
    def on_daMap_button_press_event(self, widget, event):
        x = int(event.x)
        y = int(event.y)
        
        if map and event.button == 1:
            self.map.tiles[self.layer][y/self.map.th][x/self.map.tw] = self.select
        else:
            self.map.tiles[self.layer][y/self.map.th][x/self.map.tw] = 0
        self.daMapWindow.invalidate_rect(gtk.gdk.Rectangle((x/self.map.tw)*self.map.tw, (y/self.map.th)*self.map.th, self.map.tw, self.map.th), False)
        
    def onLayerActivate(self, optmi, number):
        self.layer = number
        
        self.tbScript.set_active(False)
        self.tbCollision.set_active(False)
        
    def on_tbFillLayer_clicked(self, *args):
        fillgui = gtk.glade.XML('gui/fill.glade')
        dialog = fillgui.get_widget("filldialog")
        
        tvTiles = fillgui.get_widget("tvTiles")
        tvTiles.set_model(self.tvTilesModel)        
        
#PYGTK faq trick 13.6 - O.o
        column = gtk.TreeViewColumn()
        column.set_title('Tiles')
        tvTiles.append_column(column)
        
        renderer = gtk.CellRendererPixbuf()
        column.pack_start(renderer, expand=False)
        column.add_attribute(renderer, 'pixbuf', 0)
        
        renderer = gtk.CellRendererText()
        column.pack_start(renderer, expand=True)
        column.add_attribute(renderer, 'text', 1)
        
        response = dialog.run()
        
        if response == 0:
            (_, i) = tvTiles.get_selection().get_selected()
            if i:
                (pixbuf,iTS,iTile) = self.cursor[self.tvTilesModel.get_string_from_iter(i)]
                n = tilenumber(iTS,iTile)
                for i in xrange(self.map.h):
                    for j in xrange(self.map.w):
                        self.map.tiles[self.layer][i][j] = n
                x,y,w,h,b=self.daMapWindow.get_geometry()
                self.daMapWindow.invalidate_rect(gtk.gdk.Rectangle(0,0,w,h), False)
        dialog.destroy()
        
    def create_map(self,map):
        
        for l in self.layers: l.destroy()
        self.layers = [gtk.RadioMenuItem(None,'Layer '+str(i)) for i in range(map.nlayers)]
        
        k = 0
        for l in self.layers:
            l.show()
            l.connect('activate', self.onLayerActivate, k)
            self.menuLayer.append(l)
            k+=1
        del k
        
        for l in self.layers[1:]:
            l.set_group(self.layers[0])
        self.layers[0].set_active(True)
        
        self.tvTilesModel.clear()
        self.cursor.clear()
        self.pixtiless = []
        
        for l in xrange(len(map.tilesets.keys())):
            for t in config.tilesets:
                if t['name'] == map.tilesets[l]:
                    TS = gtk.gdk.pixbuf_new_from_file(t['image'])
                    pixbuf_tiles = []
                    for i in xrange(TS.get_height()/map.th):
                        for j in xrange(TS.get_width()/map.tw):
                            pixbuf_tiles.append(TS.subpixbuf(j*map.tw,i*map.th,map.tw,map.th))
                            
                    node = self.tvTilesModel.append(None,[None,t['name']])
                    
                    i = 0
                    for s in pixbuf_tiles:
                        v = self.tvTilesModel.append(node,[s,'tile'])
                        self.cursor[self.tvTilesModel.get_string_from_iter(v)] = (s, l, i)
                        i+=1
                        
                    self.pixtiles.append( pixbuf_tiles )
                    
        self.daMap.set_size_request(map.w*map.tw, map.h*map.th)
        
    def on_miNew_activate(self, *args):
        
        mapgui = gtk.glade.XML('gui/map.glade')
        dialog = mapgui.get_widget("dialog")
        
        fcMap = mapgui.get_widget("fcMap")
        fcMusic = mapgui.get_widget("fcMusic")
        
        tvTilesets = mapgui.get_widget("tvTilesets")
        tilesetlist = gtk.ListStore(str)
        tvTilesets.set_model(tilesetlist)
        
        column = gtk.TreeViewColumn("",gtk.CellRendererText(), text=0)
        #colunaEmail    = gtk.TreeViewColumn("Email",gtk.CellRendererText(), text=1)
        tvTilesets.append_column(column)
        
        s = tvTilesets.get_selection()
        s.set_mode(gtk.SELECTION_MULTIPLE)
        
        ref = {}
        for t in config.tilesets:
            triter = tilesetlist.append((t['name'],))
            #sometimes i really hate gtk...
            ref[tilesetlist.get_string_from_iter(triter)] = t
            
                
        response = dialog.run()
        if response == 0:
            tw = self.map.tw      = mapgui.get_widget("sbTileW").get_value_as_int()
            th = self.map.th      = mapgui.get_widget("sbTileH").get_value_as_int()
            w  = self.map.w       = mapgui.get_widget("sbMapW").get_value_as_int()
            h  = self.map.h       = mapgui.get_widget("sbMapH").get_value_as_int()
            nlayers = self.map.nlayers = mapgui.get_widget("sbLayer").get_value_as_int()
            self.map.music   = fcMusic.get_filename()
            self.map.tiles   = [numpy.zeros((h,w),'uint') for i in range(nlayers)]
            self.map.collision = numpy.zeros((h,w),'byte')
                                                
            k = 0
            (_, pathlist) = s.get_selected_rows()
            for p in pathlist:
                triter = tilesetlist.get_iter(p)
                t = ref[tilesetlist.get_string_from_iter(triter)]
                
                assert t['tilewidth'] == tw and t['tileheight'] == th, "Incorrect tile dimension"
                
                self.map.tilesets[k] = t['name']
                
                k += 1
                
            self.create_map(self.map)
            
        dialog.destroy()
        
    def set_tilesets(TSlist):
        
        self.pixtiless = []
        for t in TSlist:
            TS = gtk.gdk.pixbuf_new_from_file(t['image'])
            assert t['tilewidth'] == self.map.tw and t['tileheight'] == self.map.th, "Incorrect tile dimension"
            pixbuf_tiles = []
            for i in xrange(TS.get_height()/th):
                    for j in xrange(TS.get_width()/tw):
                        pixbuf_tiles.append(TS.subpixbuf(j*tw,i*th,tw,th))
                        
            
    def open(self,fname):
        try:
            f=open(fname,'r')
            self.map = cPickle.load(f)
            self.create_map(self.map)
        finally:
            f.close()

    def save(self,fname):
        try:
            f=open(fname,'w')
            cPickle.dump(self.map, f)        
        finally:
            f.close()

    def on_miOpen_activate(self, *args):
        fc = gtk.FileChooserDialog(title="Open Map", parent=None, action=gtk.FILE_CHOOSER_ACTION_OPEN, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
        fc.set_default_response(gtk.RESPONSE_OK)
        response = fc.run()
        if response ==  gtk.RESPONSE_OK:
            self.open(fc.get_filename())
        fc.destroy()
                
    def on_miSave_activate(self, *args):
        fc = gtk.FileChooserDialog(title="Save Map", parent=None, action=gtk.FILE_CHOOSER_ACTION_SAVE, buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_SAVE,gtk.RESPONSE_OK))
        fc.set_default_response(gtk.RESPONSE_OK)
        response = fc.run()
        if response ==  gtk.RESPONSE_OK:
            self.save(fc.get_filename())
        fc.destroy()
        
    def on_tbCollision_toggled(self, widget):
        if self.tbCollision.get_active():
            self.tbScript.set_active(False)
            
    def on_tbScript_toggled(self, widget):
        if self.tbScript.get_active():
            self.tbCollision.set_active(False)
               
if __name__ == "__main__":
    mapeditor()
