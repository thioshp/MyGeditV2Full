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

"""Methods that deal with files and directories."""

import os
import gnomevfs

def is_uri_dir(uri):
    if uri is not None and gnomevfs.exists(uri):
        file_info = gnomevfs.get_file_info(uri)
        return is_dir(file_info)
    
    return False
    
def is_dir(file_info):
    """Checks to see if the file is a directory.

    @param file_info: The file to check
    @type file_info: a gnomevfs.FileInfo

    """
    if file_info is not None: 
        return file_info.type == gnomevfs.FILE_TYPE_DIRECTORY

    return False
    
def is_file(file_info):
    """Checks to see if the file is a directory.

    @param file_info: The file to check
    @type file_info: a gnomevfs.FileInfo

    """
    if file_info is not None: 
        return file_info.type != gnomevfs.FILE_TYPE_DIRECTORY

    return False
        
def is_hidden(file_info):
    """Checks to see if the file is hidden.
    
    @param file_info: The file to check
    @type file_info: a gnomevfs.FileInfo
    
    """
    if file_info is not None:
        return file_info.name.startswith(u'.') or file_info.name.endswith(u'~')
    
    return False
    
def is_hidden_dir(file_info):
    """Checks to see if the file is a hidden directory.
    
    @param file_info: The file to check
    @type file_info: a gnomevfs.FileInfo
    
    """
    return is_dir(file_info) and is_hidden(file_info)
    
def is_hidden_file(file_info):
    """Checks to see if the file is a hidden file.
    
    @param file_info: The file to check
    @type file_info: a gnomevfs.FileInfo
    
    """
    return not is_dir(file_info) and is_hidden(file_info)
    
def is_visible_dir(file_info):
    """Checks to see if the file is a visible directory.
    
    @param file_info: The file to check
    @type file_info: a gnomevfs.FileInfo
    
    """
    return is_dir(file_info) and not is_hidden(file_info)
    
def is_visible_file(file_info):
    """Checks to see if the file is a visible file.
    
    @param file_info: The file to check
    @type file_info: a gnomevfs.FileInfo
    
    """
    return not is_dir(file_info) and not is_hidden(file_info)

def get_user_home_uri():
    """Gets a URI pointing to the user's home directory '~'."""
    return gnomevfs.URI(u'file://%s' % os.path.expanduser(u'~'))
