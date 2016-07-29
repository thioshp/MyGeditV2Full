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

import os
import sys

from gi.repository import GLib
from gi.repository import GObject
from gi.repository import Gio
from gi.repository import Gdk
from gi.repository import Gtk
from gi.repository import Pango

DATA_DIR = os.path.dirname(__file__)


class PanelHelper(GObject.GObject):
    __gsignals__ = {
        'open-file':  (GObject.SignalFlags.RUN_FIRST, None, (str,)),
    }
    
    model = None  # use one model for all windows
    scan_queue = None # if not None scan for projects is in progress
    
    def __init__ (self, config):
        GObject.GObject.__init__ (self)
        
        builder = Gtk.Builder()
        builder.add_from_file(os.path.join(DATA_DIR, 'projects.ui'))
        builder.connect_signals(self)
        
        self.widget = builder.get_object('widget_projects')
        self.treeview = builder.get_object('treeview_projects')
        self.treeview.connect('button_press_event', self.on_treeview_projects_button_press_event)
        actiongroup = builder.get_object('actiongroup_panel')
        action_refresh = builder.get_object('action_refresh')
        
        uimanager = Gtk.UIManager()
        uimanager.insert_action_group(actiongroup)
        menu_file = os.path.join(DATA_DIR, 'menu.ui')
        uimanager.add_ui_from_file(menu_file)
        self.menu_project = uimanager.get_widget('/popup_project')
        self.menu_project.attach_to_widget(self.treeview, None)
        #self.menu_project.connect('deactivate', lambda *args: self.menu_project.hide())
        
        cell = Gtk.CellRendererText(weight_set=True)
        column = Gtk.TreeViewColumn('Project', cell, text=0, weight=4)
        self.treeview.append_column(column)
        
        config.connect('refresh-projects', lambda unused: self.do_scan_projects(config))
        action_refresh.connect('activate', lambda unused: self.do_scan_projects(config))
        
        if self.model is None:
            self.__class__.model = self.treeview.get_model()
            if config.scan_on_start:
                self.do_scan_projects(config)
        else:
            self.treeview.set_model(self.model)
            
        self.active_project_tpath = None
        
    def do_scan_projects(self, config):
        if self.scan_queue is not None:
            return
        self._project_ind = config.project_indications.split()
        self.__class__.scan_queue = [(None, config.scan_location)]
        self.model.clear()
        GLib.idle_add(self._idle_scan_projects)
        
    def _idle_scan_projects(self):
        tpath, path = self.scan_queue.pop(0)
        try:
            filenames = sorted(os.listdir(path), key=str.lower)
        except OSError:
            filenames = []
        
        # check for project path
        for filename in self._project_ind:
            if filename in filenames:
                tpath = self.model.append(tpath,
                                (os.path.basename(path), path, False, False, Pango.Weight.NORMAL))
                #print '{}: {}'.format(filename, path)
                break
                
        for filename in filenames:
            if filename in self._project_ind:
                continue
            subpath = os.path.join(path, filename)
            if os.path.islink(subpath):
                continue
            if os.path.isdir(subpath):
                self.scan_queue.append((tpath, subpath))
                
        if self.scan_queue:
            return True # continue
        else:
            self.__class__.scan_queue = None
            return False
            
    def set_active_project(self, location):
        filename = location and location.get_path()
        titer_new = None
        if filename:
            titer = self.model.get_iter_first()
            while titer:
                path = self.model.get_value(titer, 1)
                if os.path.commonprefix((path, filename)) == path:
                    titer_new = titer
                    #print 'active project:', path
                    titer = self.model.iter_children(titer)
                else:
                    titer = self.model.iter_next(titer)
        if self.active_project_tpath:
            self.model[self.active_project_tpath][4] = Pango.Weight.NORMAL
        if titer_new:
            self.model.set_value(titer_new, 4, Pango.Weight.BOLD)
            self.active_project_tpath = self.model.get_path(titer_new)
            self.treeview.expand_to_path(self.active_project_tpath)
        else:
            self.active_project_tpath = None
        
    def on_treeview_projects_button_press_event(self, widget, event):
        if event.button == 3 and event.type == Gdk.EventType.BUTTON_PRESS:
            self.menu_project.popup(None, None, None, None, event.button, event.time)
        return False
        
    def on_treeview_projects_popup_menu(self, widget):
        #TODO: Open the popup at the position of the row
        #def menu_position_func(menu, unused_data):
        #    tpath, column = self.treeview.get_cursor()
        #    # How do i get the position at tpath?
        #    return x, y, True
        self.menu_project.popup(None, None, None, None, 0, Gtk.get_current_event_time())
        return True
        
    def on_action_open_directory(self, unused_action):
        tpath, unused_column = self.treeview.get_cursor()
        if tpath is None:
            return
        location = Gio.File.new_for_path(self.model[tpath][1])
        Gtk.show_uri(None, location.get_uri(), Gdk.CURRENT_TIME)
        
    def on_action_open_file(self, unused_action):
        tpath, unused_column = self.treeview.get_cursor()
        if tpath is not None:
            self.emit('open-file', self.model[tpath][1])
            
            
def main(*args):
    filename = args[1 if len(args) > 1 else 0] if args else __file__
    if filename:
        filename = os.path.abspath(filename)
    import config
    window = Gtk.Window()
    window.connect("destroy", Gtk.main_quit)
    window.set_title('Projects')
    window.resize(200, 400)
    panel = PanelHelper(config.ConfigHelper())
    panel.connect('open-file', lambda panel, filename: sys.stdout.write(filename+'\n'))
    window.add(panel.widget)
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    main(*sys.argv)
    
