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

"""Contains translation text for the plugin."""

from gettext import gettext as _

msg0001 = _(u'Project')
msg0002 = _(u'Loading...')
msg0003 = _(u'(Empty)')
msg0004 = _(u'Parent Directory')
msg0005 = _(u'Eddt')
msg0006 = _(u'A file with that name already exists, would you like to \
overwrite it?')
msg0007 = _(u'Eddt - Settings')
msg0008 = _(u'Default Repository')
msg0009 = _(u'Select Default Repository')
msg0010 = _(u'Default Terminal Emulator')
msg0011 = _(u'Terminal Arguments')
msg0012 = _(u'Default File Browser')
msg0013 = _(u'Browser Arguments')
msg0014 = _(u'File Filter')

err0001 = _(u'The project repository specified is invalid.')
err0002 = _(u'The file specified is not a file.')
err0003 = _(u'No parent window was specified.')
err0004 = _(u'The plugin has not yet been activated.')
err0005 = _(u'No ProjectExplorer was specified.')
err0006 = _(u'There was an error creating the file, no file was specified.')
err0007 = _(u'You must specify a URI.')
err0008 = _(u'You must specify an iterator on the TreeView.')
err0009 = _(u'No widget was specified.')
err0010 = _(u'A callable activate file method must be passed.')
err0011 = _(u'A callable refresh method must be passed.')
err0012 = _(u'You must specify a valid ProjectExplorer object.')
err0013 = _(u'You must specify a valid window object')
err0014 = _(u'You must specify a ProjectTreeView object.')

menu0001 = _(u'_Make Current Root')
menu0002 = _(u'_Settings')
menu0003 = _(u'Create Doc_ument...')
################################
menu0007 = _(u'Paste')
menu0008 = _(u'_Rename...')
menu0009 = _(u'Delete')
menu0010 = _(u'Create _Folder...')
menu0011 = _(u'Open Terminal _Here')

fmt0001 = _(u'Are you sure you\'d like to delete the file "%s"')
fmt0002 = _(u'There were problems deleting the file, "%s".')
fmt0003 = _(u'The folder "%s" does not exist.')
fmt0004 = _(u'The folder "%s" is not a local file.')
