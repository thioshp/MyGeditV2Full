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

"""Settings manager for Eddt."""

import os.path

import gconf
import gnomevfs

import files

class Settings(object):
    """Settings manager for Eddt."""
    
    def __init__(self):
        """Constructor."""
        super(Settings, self).__init__()
        
        self.base = u'/apps/gedit-2/plugins/eddt'
        self.client = gconf.client_get_default()
        self.client.add_dir(self.base, gconf.CLIENT_PRELOAD_NONE)
        
    def get_terminal_arguments(self):
        """Gets the options to pass to the terminal application."""
        path = os.path.join(self.base, u'terminal_arguments')
        
        val = self.client.get(path)
        
        if val is not None:
            return val.get_string()
         
        return self.set_terminal_arguments()
        
    def set_terminal_arguments(self, arguments=None):
        """Sets the arguments to pass to the terminal.
        
        @param arguments: The arguments to pass to the terminal
        @type arguments: a string
        
        """
        path = os.path.join(self.base, u'terminal_arguments')
        args = u'--working-directory=%s'
        
        if arguments is not None:
            args = arguments
        
        self.client.set_string(path, args)
        
        return args
        
    def get_browser_arguments(self):
        """Gets the options to pass to the browser application."""
        path = os.path.join(self.base, u'browser_arguments')
        
        val = self.client.get(path)
        
        if val is not None:
            return val.get_string()
         
        return self.set_browser_arguments()
        
    def set_browser_arguments(self, arguments=None):
        """Sets the arguments to pass to the browser.
        
        @param arguments: The arguments to pass to the browser
        @type arguments: a string
        
        """
        path = os.path.join(self.base, u'browser_arguments')
        args = u'%s'
        
        if arguments is not None:
            args = arguments
        
        self.client.set_string(path, args)
        
        return args
        
    def get_file_filter(self):
        """Gets the file filter used when displaying files."""
        path = os.path.join(self.base, u'file_filter')
        
        val = self.client.get(path)
        
        if val is not None:
            return val.get_string()
         
        return self.set_file_filter()
        
    def set_file_filter(self, file_filter=None):
        """Sets the default file filter.
        
        @param file_filter: The file filter to use when listing files
        @type file_filter: a string
        
        """
        path = os.path.join(self.base, u'file_filter')
        filt = u''
        
        if file_filter is not None:
            filt = file_filter
        
        self.client.set_string(path, filt)
        
        return filt
        
    def get_file_browser(self):
        """Gets the default file browser."""
        path = os.path.join(self.base, u'file_browser')
        
        val = self.client.get(path)
        
        if val is not None:
            return val.get_string()
         
        return self.set_file_browser()
        
    def set_file_browser(self, default=None):
        """Sets the default file browser.
        
        @param path: The default browser
        @type path: a string
        
        """
        path = os.path.join(self.base, u'file_browser')
        app = u'file:///usr/bin/nautilus'
        
        if default is not None:
            app = default
        
        self.client.set_string(path, str(app))
        
        return app
        
    def get_terminal(self):
        """Gets the default terminal application."""
        path = os.path.join(self.base, u'terminal')
        
        val = self.client.get(path)
        
        if val is not None:
            return val.get_string()
         
        return self.set_terminal()
        
    def set_terminal(self, default=None):
        """Sets the default terminal application.
        
        @param path: The default terminal
        @type path: a string
        
        """
        path = os.path.join(self.base, u'terminal')
        app = u'file:///usr/bin/gnome-terminal'
        
        if default is not None:
            app = default
        
        self.client.set_string(path, str(app))
        
        return app
        
    def get_repository(self):
        """Gets the default repository from GConf."""
        path = os.path.join(self.base, u'repository')
        
        val = self.client.get(path)
        
        if val is not None:
            try:
                uri = gnomevfs.URI(val.get_string())
                file_info = gnomevfs.get_file_info(uri)
                
                if files.is_dir(file_info):
                    return uri
            except:
                pass
         
        return self.set_repository()
        
    def set_repository(self, uri=None):
        """Sets the default repository in GConf.
        
        @param uri: The URI to set the default repository to
        @type uri: a gnomevfs.URI
        
        """
        path = os.path.join(self.base, u'repository')
        file_uri = files.get_user_home_uri()
        
        # Check to see if uri was specified and if it is an actual directory
        if uri is not None:
            try:
                file_info = gnomevfs.get_file_info(uri)
                
                if files.is_dir(file_info):
                    file_uri = uri
            except:
                pass
        
        self.client.set_string(path, str(file_uri))
        
        return file_uri
