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

"""A widget used to display the file/folder structure of projects."""

import gedit
import gtk
import gnomevfs

from internationalization import err0009

class Icons(object):
    """Retrieves the icons necessary for the ProjectTreeView"""
    def __init__(self, widget):
        """Constructor.
        
        @param project_treeview: The ProjectTreeView used to render the icons.
        @type project_treeview: a ProjectTreeView
        
        @raise ValueError: If a valid widget was not passed
        
        """
        if widget is None:
            raise ValueError, err0009
            
        super(Icons, self).__init__()
        
        self.__widget = widget
        self.theme = gtk.icon_theme_get_default()
        self.__initialize_icons()
    
    def retrieve_icon(self, icon_name, stock_substitute=gtk.STOCK_FILE):
        """Retrieves a rendered icon, or a substitution icon.
        
        @param icon_name: The name of the icon to load.
        @type icon_name: A string
        
        @param stock_substitute: A stock id.
        @type stock_substitute: A string
        
        @return: An icon rendered into a gtk.gdk.Pixbuf
        @rtype: A gtk.gdk.Pixbuf
        
        """
        icon = None
        
        try:
            icon = self.theme.load_icon(icon_name, 16,
                                         gtk.ICON_LOOKUP_USE_BUILTIN)
        except:
            icon = self.__widget.render_icon(
                stock_substitute, gtk.ICON_SIZE_MENU)
                
        return icon
        
    def retrieve_file_icon(self, uri):
        """Retrieves a rendered icon based on mime-type and theme.
        
        @param uri: The URI of a file.
        @type uri: A string
        
        @return: An icon rendered into a gtk.gdk.Pixbuf
        @rtype: A gtk.gdk.Pixbuf
        
        """
        mime_type = gnomevfs.get_mime_type(str(uri))
        icon_name = self.__make_icon_mime_name(mime_type)
        icon = None
        
        try:
            icon = self.theme.load_icon(icon_name, 16,
                                         gtk.ICON_LOOKUP_USE_BUILTIN)
        except:
            icon = self.file
                
        return icon
     
    def __initialize_icons(self):
        """Retrieves and initializes the icons.""" 
        self.folder = self.retrieve_icon(u'stock_folder', gtk.STOCK_DIRECTORY)
        self.folder_open = self.retrieve_icon(u'stock_open', gtk.STOCK_OPEN)
        self.folder_parent = self.retrieve_icon(u'stock_go_back',
                                                gtk.STOCK_GO_BACK)
        self.file = self.retrieve_icon(u'stock_file')
        
    def __make_icon_mime_name(self, mime_type):
        """Format a mime-type into an icon name.
        
        @param mime_type: A mime-type name
        @type mime_type: A string
        
        @return: A formatted string used as a mime-type icon name.
        @rtype: A string
        
        """
        return "gnome-mime-%s" % mime_type.replace(u'/', u'-')
