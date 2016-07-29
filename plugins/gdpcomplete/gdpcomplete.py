"""CompletePlugin enabled word and symbol completion."""
# Copyright (C) 2007-2012 - Curtis Hovey <sinzui.is at verizon.net>
# This software is licensed under the GNU General Public License version 2
# (see the file COPYING).

__all__ = [
    'CompletePlugin',
    ]

from gettext import gettext as _
import os

from gi.repository import (
    GObject,
    Gtk,
    PeasGtk,
    )

from gdpbase import (
    GDPPluginMixin,
    Gedit,
    )
from gdp import config
from gdp.complete import Completer


class CompletePlugin(GDPPluginMixin,
                            GObject.Object, Gedit.WindowActivatable,
                            PeasGtk.Configurable):
    """Automatically complete words from the list of words in the document."""
    __gtype_name__ = "GDPCompletePlugin"
    window = GObject.property(type=Gedit.Window)

    CONTROLLER_CLASS = Completer
    ACTION_GROUP_NAME = 'GDPSyntaxActions'
    MENU_PATH = '/MenuBar/ToolsMenu/ToolsOps_2/CompleteWord'
    MENU_XML = """
        <ui>
          <menubar name="MenuBar">
            <menu name='ToolsMenu' action='Tools'>
              <placeholder name="ToolsOps_2">
                <separator />
                <menuitem action="CompleteWord"/>
                <menuitem action="SuggestCompletions"/>
                <separator />
              </placeholder>
            </menu>
          </menubar>
        </ui>
        """

    def actions(self, syntaxer):
        """See `GDPPluginMixin`"""
        return  [
            ('CompleteWord', None, _("Complete _word"),
                config.get('completer', 'show_accel'),
                _("Complete the word at the cursor."),
                syntaxer.show_completion),
            ('SuggestCompletions', None, _("Suggest completions"),
                None, _("Suggest completions as words are typed."),
                syntaxer.on_suggest_completions_toggled,
                config.getboolean('completer', 'suggest_completions')),
            ]

    def __init__(self):
        """Initialize the plugin the whole Gedit application."""
        GObject.Object.__init__(self)
        self.controller = None

    def do_activate(self):
        self.activate()
        self.connect_signal(
            self.window, 'tab-added', self.on_tab_added_or_changed)
        self.connect_signal(
            self.window, 'active-tab-changed', self.on_tab_added_or_changed)

    def do_update_state(self):
        if config.do_update_state:
            # This updated the accel, but the menu does not show it.
            memonic = config.get('completer', 'show_accel')
            keyval, modifiers = Gtk.accelerator_parse(memonic)
            Gtk.AccelMap.change_entry(
                "<Actions>/GDPSyntaxActions/CompleteWord",
                keyval, modifiers, False)
            action = self.action_group.get_action('CompleteWord')
            self.action_group.remove_action(action)
            self.action_group.add_action_with_accel(action, memonic)
            config.do_update_state = False

    def do_deactivate(self):
        self.deactivate()

    def do_create_configure_widget(self):
        # This is an unactivated instance.
        widgets = self._get_configure_widgets()
        grid = widgets.get_object('preferences')
        return grid

    def _get_configure_widgets(self):
        # This is an unactivated instance.
        widgets = Gtk.Builder()
        widgets.add_from_file(
            '%s/gdp/complete.ui' % os.path.dirname(__file__))
        entry = widgets.get_object('shortcut_entry')
        entry.set_text(config.get('completer', 'show_accel'))
        widgets.connect_signals(
            {'on_focus_out_event': self.on_focus_out_event})
        return widgets

    def on_focus_out_event(self, entry, data=None):
        # This is an unactivated instance.
        shortcut = entry.get_text()
        if shortcut != config.get('completer', 'show_accel'):
            config.set('completer', 'show_accel', shortcut)
            config.dump()
            config.do_update_state = True

    def on_tab_added_or_changed(self, window, tab):
        """Callback method for tab-added or active-tab-changed window signal.

        Correct the language and update the menu.
        """
        self.controller.correct_language(tab.get_document())
        view = tab.get_view()
        if view == window.get_active_view():
            self.controller.set_view(view)
            manager = self.window.get_ui_manager()
            manager.get_action(self.MENU_PATH).props.sensitive = True
