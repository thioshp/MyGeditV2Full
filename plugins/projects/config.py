# -*- coding: utf-8 -*-

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


import os
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import Gio

ui_file = os.path.join(os.path.dirname(__file__), 'config.ui')
settings_schema = "org.gnome.gedit.plugins.projects"


class ConfigHelper (GObject.GObject):
    __gsignals__ = {
        'refresh-projects':  (GObject.SignalFlags.RUN_FIRST, None, ()),
    }
    
    def __init__(self):
        GObject.GObject.__init__(self)
        self.settings = Gio.Settings.new(settings_schema)
        
    def create_widget(self, window):
        builder = Gtk.Builder()
        builder.add_from_file(ui_file)
        builder.connect_signals(self)
        entry_scandir = builder.get_object('entry_scandir')
        button_scandir = builder.get_object('button_scandir')
        button_refresh = builder.get_object('button_refresh')
        button_clear_indfiles = builder.get_object('button_clear_indications')
        
        self.settings.bind("scan-location",
                           entry_scandir, 'text',
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("project-indications",
                           builder.get_object('entry_indications'), 'text',
                           Gio.SettingsBindFlags.DEFAULT)
        self.settings.bind("scan-on-start",
                           builder.get_object('checkbutton_scan_on_start'), 'active',
                           Gio.SettingsBindFlags.DEFAULT)
                           
        def on_button_scandir(button):
            dialog = Gtk.FileChooserDialog("Select Folder",
                                          window,
                                          Gtk.FileChooserAction.SELECT_FOLDER,
                                          [Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                          Gtk.STOCK_OPEN, Gtk.ResponseType.ACCEPT])
            dialog.set_current_folder(self.scan_location)
            if dialog.run() == Gtk.ResponseType.ACCEPT:
                self.scan_location = dialog.get_filename()
            dialog.destroy()
        button_scandir.connect('clicked', on_button_scandir)
        def on_button_button_clear_indfiles(unused_button):
            self.settings.reset("project-indications")
        button_clear_indfiles.connect('clicked', on_button_button_clear_indfiles)
        def on_button_refresh(unused_button):
            self.emit('refresh-projects')
        button_refresh.connect('clicked', on_button_refresh)
        
        widget = builder.get_object('widget_projects')
        return widget
        
    scan_location = property(
        lambda self: self.settings.get_string("scan-location"),
        lambda self, value: self.settings.set_string("scan-location", value))
    project_indications = property(
        lambda self: self.settings.get_string("project-indications"),
        lambda self, value: self.settings.set_string("project-indications", value))
    scan_on_start = property(
        lambda self: self.settings.get_boolean("scan-on-start"),
        lambda self, value: self.settings.set_boolean("scan-on-start", value))
        
        
def main():
    dialog = Gtk.Dialog("Message",
                        None,
                        Gtk.DialogFlags.MODAL,
                        [Gtk.STOCK_CLOSE, Gtk.ResponseType.NONE])
    area = dialog.get_content_area()
    config = ConfigHelper()
    area.add(config.create_widget(dialog))
    dialog.run()
    dialog.destroy()
    
if __name__ == '__main__':
    main()
    
