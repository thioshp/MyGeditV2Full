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

"""The management class of the plugin, it is used to construct, activate,
deactivate, and update the plugin.

"""

import os
import os.path

import gtk
import gnomevfs
import gobject
import gedit

import files
import dialogs
from internationalization import fmt0001, fmt0002, fmt0003, fmt0004, \
                                 err0001, err0013, err0014
from settings import Settings
from settingsdialog import SettingsDialog

class ProjectExplorer(object):
    """Manages all aspects of the plugin including activation, deactivation,
    and udating the UI.
    
        pe.get_window()
        pe.get_settings()
        pe.get_repository()
        pe.refresh()
        pe.navigate_to_parent()
        pe.set_repository(uri)
        pe.open_file(uri)
        pe.open_terminal(uri)
        pe.create_file_in(uri)
        pe.create_folder_in(uri)
        pe.unlink(uri)
        pe.display_settings()
    
    """
    
    def __init__(self, window, tree_view):
        """Constructor.
        
        Initializes the plugin.
        
        @param window: the Gedit window the plugin should be associated with.
        @type window: a gedit.Window
        
        @raise ValueError: if a valid window or treeview was not passed
        
        """
        if window is None:
            raise ValueError, err0013 
            
        if tree_view is None:
            raise ValueError, err0014       
        
        super(ProjectExplorer, self).__init__()
        
        self.__window = window
        self.__tree_view = tree_view

        # Set up signal handlers
        self.__tree_view.set_activate_file(
            lambda d: self.open_file(d.get_uri()))
        self.__tree_view.set_refresh(
            lambda: self.set_repository(self.get_repository(), True))
        
        self.__settings = Settings()
        self.__encoding = gedit.gedit_encoding_get_current()
        
    def display_settings(self):
        """Display a dialog box with plugin settings."""
        dialog = SettingsDialog(self)
        dialog.run()
        self.refresh()
        
    def get_window(self):
        """Gets the Gedit window associated with the plugin.
        
        @returns: The Gedit window associated with the plugin
        @rtype: a gedit.Window
        
        """
        return self.__window
        
    def get_settings(self):
        """Gets the Settings object.
        
        @returns: The Settings object associated with the plugin
        @rtype: a Settings object
        
        """
        return self.__settings
        
    def refresh(self):
        """Refreshes the current view."""
        if self.__tree_view is None:
            return None
        else:
            return self.__tree_view.refresh()
        
    def open_terminal(self, uri):
        """Opens a terminal at the specified location.
        
        @param uri: The local URI to open the terminal to.
        @type uri: a gnomevfs.URI
        
        """
        message = None
        
        if not gnomevfs.exists(uri):
            message = fmt0003 % uri
        elif not uri.is_local:
            message = fmt0004 % uri
        
        if message is not None:
            dialogs.error(message)
            return
            
        local_path = uri.path
        app = gnomevfs.URI(self.get_settings().get_terminal()).path
        args = self.get_settings().get_terminal_arguments()
        
        os.spawnlp(os.P_NOWAIT, app, app, args % local_path)
        
    def open_file_browser(self, uri):
        """Opens a file browser at the specified location.
        
        @param uri: The local URI to open the file browser to.
        @type uri: a gnomevfs.URI
        
        """
        message = None
        
        if not gnomevfs.exists(uri):
            message = fmt0003 % uri
        elif not uri.is_local:
            message = fmt0004 % uri
        
        if message is not None:
            dialogs.error(message)
            return
            
        local_path = uri.path
        app = gnomevfs.URI(self.get_settings().get_file_browser()).path
        args = self.get_settings().get_browser_arguments()
        
        os.spawnlp(os.P_NOWAIT, app, app, args % local_path)
    
    def create_file_in(self, uri):
        """Launches a new file dialog box set to create a new file within
        the URI specified.
        
        @param uri: The local URI to create the file in
        @type uri: a gnomevfs.URI
        
        """
        try:
            file_uri = dialogs.retrieve_new_file_name(uri)
            
            if file_uri is not None:
                newfile = gnomevfs.create(file_uri,
                                          open_mode=gnomevfs.OPEN_WRITE)
                newfile.truncate(0)
                newfile.close()
                
        except IOError, e:
            dialog.error(e)
        
        self.refresh()
    
    def create_folder_in(self, uri):
        """Launches a new folder dialog box set to create a new folder within
        the URI specified.
        
        @param uri: The local URI to create the folder in
        @type uri: a gnomevfs.URI
        
        """
        dialog = gtk.FileChooserDialog(
            action=gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER)
        
        dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                           gtk.STOCK_ADD, gtk.RESPONSE_OK)
                     
        dialog.set_current_folder_uri(str(uri))
        
        response = dialog.run()
        folder_uri = dialog.get_uri()
        dialog.destroy()
        
        self.refresh()
         
    def unlink(self, uri):
        """Deletes the specified URI.
        
        @param uri: The URI to delete.
        @type uri: a gnomevfs.URI
        
        """
        # Be sure the file exists then delete it
        if gnomevfs.exists(uri):
            file_info = gnomevfs.get_file_info(uri)
            
            # Double check the user wants to delete the file
            response = dialogs.choice_ok_cancel(fmt0001 % str(uri), True)
            
            if response == gtk.RESPONSE_OK:
                try:
                    if files.is_dir(file_info):
                        self.__remove_directory(uri)
                    else:
                        gnomevfs.unlink(uri)
                        
                except Exception, e:
                    dialogs.error(fmt0002 % e)
                    
                self.refresh()

    def get_repository(self):
        """Gets the URI associated with the currently opened repository.
        
        @return: The URI associated with the currently opened repository,
            if no repository is currently opened then it returns None.
        @rtype: a gnomevfs.URI or None
        
        """
        if self.__tree_view is None:
            return None
        else:
            return self.__tree_view.get_repository()
                    
    def set_repository(self, uri=None, force=False):
        """Sets the repository to be viewed.
        
        @param uri: The URI to set the repository to.
        @type uri: a gnomevfs.URI
        
        @param force: Should the repository be forced to refresh.
        @type force: a boolean
        
        @raise ValueError: If the URI passed does not exist, or if the URI does
            not point to a directory.
        
        """
        # Set the URI to the user's home directory if no URI was passed
        if uri is None:
            uri = self.get_settings().get_repository()
            
        # Error if the file passed does not exist or is not a directory
        if not gnomevfs.exists(uri):
            raise ValueError, err0001
        
        directory = gnomevfs.get_file_info(uri)
        
        if not files.is_dir(directory):
            raise ValueError, err0001
        
        # Do nothing if the repository passed is the current repository and
        # the set was not forced
        if not force and str(uri) == str(self.get_repository()):
            return
        
        # Record what the default repository is in the settings
        self.get_settings().set_repository(uri)
        
        self.__tree_view.set_repository(uri)
     
    def open_file(self, uri):
        """Opens a file in Gedit.
        
        @param uri: the URI of the file.
        @type uri: a gnomevfs.URI
        
        """
        # Open the file within the current tab if the current tab is an
        # untitled and untouched file.
        tab = self.__window.get_active_tab()
        
        if tab is not None:
            document = tab.get_document()
                
            if document.is_untitled() and document.is_untouched():
                document.load(str(uri), self.__encoding, 0, False)
                self.__window.set_active_tab(tab)
                return
        
        # Open the document in a new tab    
        self.__window.create_tab_from_uri(str(uri),
                                        self.__encoding,
                                        0, False, True)
                                        
    def navigate_to_parent(self):
        """Navigates to the current repository's parent directory."""
        uri = self.get_repository()
        
        if uri is not None:
            parent = uri.parent
            
            if files.is_uri_dir(parent):
                self.set_repository(parent)
                    
    def __remove_directory(self, uri):
        """Deletes a folder recursively.
        
        @param uri: the URI of the folder to delete.
        @type uri: a gnomevfs.URI
        
        """
        directory = gnomevfs.DirectoryHandle(uri)
        
        for file_info in directory:
            file_uri = uri.append_file_name(file_info.name)
            
            is_self = file_uri == uri
            is_parent = bool(file_uri.is_parent(uri, False))

            if not is_self and not is_parent:
                if files.is_dir(file_info):
                    self.__remove_directory(file_uri)
                else:
                    gnomevfs.unlink(file_uri)
        
        gnomevfs.remove_directory(uri)
