# Copyright (C) 2011-2012 - Curtis Hovey <sinzui.is at verizon.net>
# This software is licensed under the GNU General Public License version 2
# (see the file COPYING).
"""GDP Gedit Developer Plugin base."""

__all__ = [
    'GDPPluginMixin',
    ]

from gi.repository import (
    GObject,
    Gio,
    Gtk,
    )

import os
use_fake_gedit = os.environ.get('use_fake_gedit') == 'true'
if use_fake_gedit:
    from testing import Gedit
    # Hush lint.
    Gedit
else:
    from gi.repository import Gedit
from gdp import (
    config,
    CONFIG_VERSION,
    )


# Signals shared in GDP.

GObject.signal_new(
    'syntax-error-python', Gedit.Document, GObject.SIGNAL_RUN_LAST,
    GObject.TYPE_NONE, ())


GObject.signal_new(
    'bzr-branch-open', Gedit.Window, GObject.SIGNAL_RUN_LAST,
    GObject.TYPE_NONE, (GObject.TYPE_STRING, ))


# Common GDP classes.


class GDPPluginMixin:
    """Decorate a `GeditWindow` with GDP state"""

    ACTION_GROUP_NAME = None
    MENU_XML = None

    def actions(self, controller):
        """Return a list of action tuples.

        (name, stock_id, label, accelerator, tooltip, callback)
        or
        (name, stock_id, label, accelerator, tooltip, callback, is_active)
        """
        pass

    def activate(self):
        if do_migrate_settings():
            migrate_settings()
        self.signal_ids = {}
        self.ui_id = None
        self.controller = self.CONTROLLER_CLASS(self.window)
        if self.ACTION_GROUP_NAME is None:
            return
        self.action_group = Gtk.ActionGroup(name=self.ACTION_GROUP_NAME)
        self.action_group.set_translation_domain('gedit')
        actions = self.actions(self.controller)
        self.action_group.add_actions(
            [a for a in actions if len(a) == 6])
        self.action_group.add_toggle_actions(
            [a for a in actions if len(a) == 7])
        manager = self.window.get_ui_manager()
        manager.insert_action_group(self.action_group, -1)
        self.ui_id = manager.add_ui_from_string(self.MENU_XML)

    def deactivate(self):
        """Deactivate the plugin for the window."""
        if self.ui_id is None:
            return
        manager = self.window.get_ui_manager()
        manager.remove_ui(self.ui_id)
        manager.remove_action_group(self.action_group)
        manager.ensure_update()
        self.controller.deactivate()
        self.controller = None

    def connect_signal(self, obj, signal, method):
        """Connect the signal from the provided object to a method."""
        if obj is None:
            return
        self.signal_ids[signal] = obj.connect(signal, method)

    def connect_signal_after(self, obj, signal, method):
        """Connect the signal from the provided object to a method."""
        if obj is None:
            return
        self.signal_ids[signal] = obj.connect_after(signal, method)

    def disconnect_signal(self, obj, signal):
        """Disconnect the signal from the provided object."""
        if obj is None:
            return
        if signal in self.signal_ids:
            obj.disconnect(self.signal_ids[signal])
            del self.signal_ids[signal]

    @property
    def active_document(self):
        """The active document in the window."""
        self.window.get_active_document()


def do_migrate_settings():
    if not config._loaded_file_path:
        return True
    try:
        version = config.getint('gdp', 'version')
    except:
        return True
    else:
        if version < CONFIG_VERSION:
            return True
    return False


def migrate_settings():
    """Update settings to the current version of GDP."""
    old_completer = 'gdpsyntaxcompleter'
    new_completer = 'gdpcomplete'
    settings = Gio.Settings.new('org.gnome.gedit.plugins')
    active_plugins = settings.get_strv('active-plugins')
    if old_completer in active_plugins:
        # Remove the old completer and maybe replace it with the new one.
        index = active_plugins.index(old_completer)
        active_plugins.remove(old_completer)
        if new_completer not in active_plugins:
            active_plugins.insert(index, new_completer)
        settings.set_strv('active-plugins', active_plugins)
    return active_plugins
