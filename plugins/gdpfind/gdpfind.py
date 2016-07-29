# Copyright (C) 2008-2012 - Curtis Hovey <sinzui.is at verizon.net>
# This software is licensed under the GNU General Public License version 2
# (see the file COPYING).
"""Find matching text in multiple files."""

__all__ = [
    'FindPlugin',
    ]


from gettext import gettext as _

from gi.repository import GObject

from gdpbase import (
    GDPPluginMixin,
    Gedit,
    )
from gdp.find import Finder


class FindPlugin(GDPPluginMixin, GObject.Object, Gedit.WindowActivatable):
    """Find matching text in multiple files plugin."""
    __gtype_name__ = "GDPFindPlugin"
    window = GObject.property(type=Gedit.Window)

    CONTROLLER_CLASS = Finder
    ACTION_GROUP_NAME = 'GDPFindActions'
    MENU_XML = """
        <ui>
          <menubar name="MenuBar">
            <menu name="SearchMenu" action='Search'>
              <placeholder name="SearchOps_5">
                <separator/>
                <menuitem action="FindFiles"/>
                <menuitem action="ReplaceFiles"/>
                <separator/>
              </placeholder>
            </menu>
          </menubar>
        </ui>
        """

    def actions(self, finder):
        """See `GDPPluginMixin`"""
        return [
            ('FindFiles', None, _('Find in files...'),
                '<Control><Shift>f', _('Fi_nd in files'),
                finder.show),
            ('ReplaceFiles', None, _('R_eplace in files...'),
                '<Control><Shift>h', _('Replace in files'),
                finder.show_replace),
            ]

    def __init__(self):
        """Initialize the plugin the whole Gedit application."""
        GObject.Object.__init__(self)
        self.controller = None

    def do_activate(self):
        """Activate the plugin in the current top-level window.

        Add 'Find in files' to the menu.
        """
        self.activate()
        self.connect_signal(
            self.window, 'bzr-branch-open',
            self.controller.on_file_path_added)

    def do_deactivate(self):
        """Deactivate the plugin in the current top-level window.

        Remove a 'Find in files' to the menu.
        """
        self.deactivate()

    def do_update_state(self):
        """Toggle the plugin's sensativity in the top-level window.

        'Find in files' is always active.
        """
        pass
