# -*- coding:utf-8 -*-

#  Copyright © 2012  B. Clausius <barcc@gmx.de>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


from gi.repository import Gedit
from gi.repository import GObject
from gi.repository import GLib
from gi.repository import Gio
from gi.repository import Gtk
from gi.repository import PeasGtk

from projects.panel import PanelHelper
from projects.config import ConfigHelper


class ProjectsWindow(GObject.Object, Gedit.WindowActivatable, PeasGtk.Configurable):
    __gtype_name__ = "ProjectsWindow"
    window = GObject.property(type=Gedit.Window)
    config = None
    
    def __init__(self):
        GObject.Object.__init__(self)
        self.panel_helper = None
        self.handlers = []
        
    def do_activate(self):
        if self.config is None:
            self.__class__.config = ConfigHelper()
        
        self.panel_helper = PanelHelper(self.config)
        icon = Gtk.Image.new_from_icon_name('applications-development', Gtk.IconSize.MENU)
        panel = self.window.get_side_panel()
        panel.add_item(self.panel_helper.widget, "ProjectsSidePanel", "Projects", icon)
        
        self._connect('tab-added', self.on_window_tab_added)
        self._connect('active-tab-changed', self.on_window_tab_changed)
        self._connect('tab-removed', self.on_window_tab_removed)
        self.panel_helper.connect('open-file', self.on_panel_open_file)
        
    def do_deactivate(self):
        self._disconnect_all()
        
        panel = self.window.get_side_panel()
        panel.remove_item(self.panel_helper.widget)
        self.panel_helper = None
        
    #def do_update_state(self):
    #    pass
        
    def do_create_configure_widget(self):
        if self.config:
            return self.config.create_widget(self.window)
        else:
            return Gtk.Label('Hm …\nconfig not found.')
        
    def _connect(self, signal, func):
        self.handlers.append(self.window.connect(signal, func))
    def _disconnect_all(self):
        for handler in self.handlers:
            self.window.disconnect(handler)
            
    def on_window_tab_added(self, unused_window, unused_tab):
        pass
    def on_window_tab_changed(self, unused_window, tab):
        doc = tab.get_document()
        location = doc and doc.get_location()
        self.panel_helper.set_active_project(location)
    def on_window_tab_removed(self, unused_window, unused_tab):
        pass
        
    def on_panel_open_file(self, panel, dirname):
        dialog = Gtk.FileChooserDialog("Open File",
                                      self.window,
                                      Gtk.FileChooserAction.OPEN,
                                      [Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                      Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT])
        dialog.set_current_folder(dirname)
        if dialog.run() == Gtk.ResponseType.ACCEPT:
            filename = dialog.get_filename()
            location = Gio.File.new_for_path(filename)
            tab = self.window.get_tab_from_location(location)
            if tab is None:
                tab = self.window.create_tab_from_location(location, None, 0, 0, False, True)
            else:
                self.window.set_active_tab(tab)
            GObject.idle_add(tab.get_view().grab_focus)
        dialog.destroy()
        
