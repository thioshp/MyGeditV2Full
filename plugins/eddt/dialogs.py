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

"""Methods that deal with launching dialogs."""

import gtk
import gnomevfs

import files
from internationalization import msg0006, err0006
          
def error(message):
    """Displays on error dialog with a single stock OK button.
    
    @param message: The message to display in the error message dialog.
    @type message: a string
    
    """
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               gtk.MESSAGE_ERROR,
                               gtk.BUTTONS_OK,
                               message)
    
    response = dialog.run()
    dialog.destroy()
    
def choice_ok_cancel(message, cancelDefault=False):
    """Displays an ok/cancel message dialog.
    
    @param message: The message to display in the ok/cancel message dialog.
    @type message: a string
    
    @param cancelDefault: Whether gtk.RESPONSE_CANCEL is the default response.
    @type cancelDefault: a boolean
    
    @returns: gtk.RESPONSE_OK or gtk.RESPONSE_CANCEL
    @rtype: a gtk response object
    
    """
    default = gtk.RESPONSE_OK
    
    if cancelDefault:
        default = gtk.RESPONSE_CANCEL
    
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               gtk.MESSAGE_QUESTION,
                               gtk.BUTTONS_OK_CANCEL,
                               message)
                               
    dialog.set_default_response(default)
        
    response = dialog.run()
    dialog.destroy()
    
    return response
    
def choice_yes_no(message, noDefault=False):
    """Displays an yes/no message dialog.
    
    @param message: The message to display in the yes/no message dialog.
    @type message: a string
    
    @param noDefault: Whether gtk.RESPONSE_NO is the default response.
    @type noDefault: a boolean
    
    @returns: gtk.RESPONSE_YES or gtk.RESPONSE_NO
    @rtype: a gtk response object
    
    """
    default = gtk.RESPONSE_YES
    
    if noDefault:
        default = gtk.RESPONSE_NO
    
    dialog = gtk.MessageDialog(None,
                               gtk.DIALOG_MODAL,
                               gtk.MESSAGE_QUESTION,
                               gtk.BUTTONS_YES_NO,
                               message)
                               
    dialog.set_default_response(default)
        
    response = dialog.run()
    dialog.destroy()
    
    return response

def retrieve_new_file_name(uri=None):
    """Get the name of a file to create.
    
    @param uri: The URI of the folder to begin in
    @type uri: a gnomevfs.URI
    
    @raise IOError: if there was a problem retrieving the file URI
    
    """
    dialog = gtk.FileChooserDialog(action=gtk.FILE_CHOOSER_ACTION_SAVE)
    
    dialog.add_buttons(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                       gtk.STOCK_ADD, gtk.RESPONSE_OK)
    
    # Default to the users home directory
    if uri is None:
        uri = files.get_user_home_uri()
        
    dialog.set_current_folder_uri(str(uri))
    
    # Get the response and the URI
    response = dialog.run()
    file_uri = dialog.get_uri()
    dialog.destroy()
    
    if response == gtk.RESPONSE_OK:
        if file_uri is not None:
            write = True
            
            # Check to be sure if the user wants to overwrite a file
            if gnomevfs.exists(file_uri):
                response = choice_yes_no(msg0006, True)
                
                if response == gtk.RESPONSE_NO:
                    write = False
            
            if write:
                # Return the new filename
                return file_uri
        else:
            raise IOError, err0006
    
    return None
