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

"""A description of a found path within the ProjectTreeView"""

import os.path

from internationalization import err0007, err0008
    
class PathDescriptor(object):
    """Describes the location of a file within the ProjectTreeView."""
    
    def __init__(self, uri, isdir=False):
        """Constructor.
        
        @param uri: the uri of the file.
        @type uri: a gnomevfs.URI
        
        @param isdir: whether the file is a directory.
        @type isdir: a boolean
                
        """            
        self.__uri = uri
        self.__tree_iter = None
        self.__isdir = isdir
        
    def get_uri(self):
        """Gets a URI pointing to a location on the file system.
        
        @return: a URI pointing to a location on the file system
        @rtype: a gnomevfs.URI
        
        """
        return self.__uri
        
    def get_name(self):
        """Gets the display name.
        
        @return: the display name
        @rtype: a string
        
        """
        return self.__uri.short_name
        
    def get_iter(self):
        """Gets an iterator from the TreeView.
        
        @return: an iterator on the TreeView
        @rtype: a gtk.TreeIter
        
        """
        return self.__tree_iter
        
    def set_iter(self, tree_iter):
        """Sets an iter from the TreeView.
        
        @param tree_iter: an iterator on the TreeView
        @type tree_iter: a gtk.TreeIter
        
        """            
        self.__tree_iter = tree_iter
        
    def is_dir(self):
        """Gets whether the descriptor corresponds with a directory.
        
        @return: whether the descriptor corresponds with a directory
        @rtype: a boolean
        
        """
        return self.__isdir
