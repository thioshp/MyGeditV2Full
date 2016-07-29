# -*- coding: utf-8 -*-
# Eddt is a directory browsing plugin written in Python for the Gnome text 
# editor, gedit.
#
# Copyright (C) 2006 Michael Diolosa <michael@mbrio.org>

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA.

"""Dialog that manages settings."""

import gtk

from internationalization import err0012, msg0007, msg0008, msg0009, \
                                 msg0010, msg0011, msg0012, msg0013, msg0014

class SettingsDialog(gtk.Dialog):
    """Dialog that manages settings."""
    
    def __init__(self, eddt):
        """Constructor.
        
        @param eddt: The ProjectExplorer to associate with the settings.
        @type eddt: a ProjectExplorer
        
        @raise ValueError: When a valid ProjectExplorer has not been supplied.
        
        """
        if eddt is None:
            raise ValueError, err0012
            
        # Ititialize self
        flags = gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT
        super(SettingsDialog, self).__init__(title=msg0007,
                                             flags=flags)
        
        self.__eddt = eddt
        self.set_property(u'resizable', False)
        
        settings = self.__eddt.get_settings()
        
        table = gtk.Table(rows=4, columns=2, homogeneous=False)
        table.set_row_spacings(5)
        table.set_col_spacings(10)
        
        # Default Repository
        label = gtk.Label(msg0008)
        label.set_property(u'xalign', 0.0)
        table.attach(label, 0, 1, 0, 1)
        
        widget = gtk.FileChooserButton(msg0009)
        widget.set_property(u'width-request', 300)
        widget.set_action(gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER)
        widget.set_uri(str(settings.get_repository()))
        
        self.__default_repository = widget
        
        table.attach(widget, 1, 2, 0, 1)    
        
        # Default Terminal Emulator
        label = gtk.Label(msg0010)
        label.set_property(u'xalign', 0.0)
        table.attach(label, 0, 1, 1, 2)
        
        widget = gtk.FileChooserButton(msg0010)
        widget.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        widget.set_uri(str(settings.get_terminal()))
        
        self.__default_terminal = widget
        
        table.attach(widget, 1, 2, 1, 2)

        # Terminal Arguments        
        label = gtk.Label(msg0011)
        label.set_property(u'xalign', 0.0)
        table.attach(label, 0, 1, 2, 3)
        
        widget = gtk.Entry()
        widget.set_text(settings.get_terminal_arguments())
        
        self.__default_terminal_arguments = widget
        
        table.attach(widget, 1, 2, 2, 3)
        
        # Default File Browser
        label = gtk.Label(msg0012)
        label.set_property(u'xalign', 0.0)
        table.attach(label, 0, 1, 3, 4)
        
        widget = gtk.FileChooserButton(msg0012)
        widget.set_action(gtk.FILE_CHOOSER_ACTION_OPEN)
        widget.set_uri(str(settings.get_file_browser()))
        
        self.__default_file_browser = widget
        
        table.attach(widget, 1, 2, 3, 4)

        # Browser Arguments        
        label = gtk.Label(msg0013)
        label.set_property(u'xalign', 0.0)
        table.attach(label, 0, 1, 4, 5)
        
        widget = gtk.Entry()
        widget.set_text(settings.get_browser_arguments())
        
        self.__default_browser_arguments = widget
        
        table.attach(widget, 1, 2, 4, 5)

        # File Filter        
        label = gtk.Label(msg0014)
        label.set_property(u'xalign', 0.0)
        table.attach(label, 0, 1, 5, 6)
        
        widget = gtk.Entry()
        widget.set_text(settings.get_file_filter())
        
        self.__default_file_filter = widget
        
        table.attach(widget, 1, 2, 5, 6)
        
        self.vbox.pack_start(table, True, True, 0)
        
        self.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
        self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)

        self.connect(u'response', self.__on_response)
        
        self.show_all()

    def __on_response(self, dialog, response_id, data=None):
        """Handles the choice made by the dialog."""
        # If the dialog choices were ok then save all settings
        if response_id == gtk.RESPONSE_OK:
            settings = self.__eddt.get_settings()
            settings.set_repository(self.__default_repository.get_uri())
            settings.set_terminal(self.__default_terminal.get_uri())
            settings.set_terminal_arguments(
                self.__default_terminal_arguments.get_text())
            settings.set_file_browser(self.__default_file_browser.get_uri())
            settings.set_browser_arguments(
                self.__default_browser_arguments.get_text())
            settings.set_file_filter(self.__default_file_filter.get_text())
            
        self.destroy()
