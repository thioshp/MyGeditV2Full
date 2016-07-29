# Copyright (C) 2009-2012 - Curtis Hovey <sinzui.is at verizon.net>
# This software is licensed under the GNU General Public License version 2
# (see the file COPYING)."""Text formatting features for the edit menu."""

__all__ = [
    'FormatPlugin',
    ]


from gettext import gettext as _

from gi.repository import GObject

from gdpbase import (
    GDPPluginMixin,
    Gedit,
    )
from gdp import config
from gdp.format import Formatter


class FormatPlugin(GDPPluginMixin, GObject.Object, Gedit.WindowActivatable):
    """Plugin for formatting code."""
    __gtype_name__ = "GDPFormatPlugin"
    window = GObject.property(type=Gedit.Window)

    CONTROLLER_CLASS = Formatter
    ACTION_GROUP_NAME = 'GDPFormatActions'
    MENU_XML = """
        <ui>
          <menubar name="MenuBar">
            <menu name='EditMenu' action='Edit'>
              <placeholder name="EditOps_3">
                  <separator />
                  <menu action="GDPFormatMenu">
                    <menuitem action="RewrapText"/>
                    <menuitem action="FixLineEnding"/>
                    <menuitem action="TabsToSpaces"/>
                    <menuitem action="QuoteLines"/>
                    <menuitem action="SortImports"/>
                    <menuitem action="SingleLine"/>
                    <menuitem action="REReplace"/>
                  </menu>
                  <separator />
              </placeholder>
            </menu>
            <menu name='ToolsMenu' action='Tools'>
              <placeholder name="ToolsOps_2">
                <separator />
                <menuitem action="CheckProblems"/>
                <menuitem action="CheckAllProblems"/>
                <menuitem action="ShowSyntaxErrorsOnly"/>
                <menuitem action="ReformatDoctest"/>
                <menuitem action="ReformatCSS"/>
                <separator />
              </placeholder>
            </menu>
          </menubar>
        </ui>
        """

    def actions(self, formatter):
        """See `GDPPluginMixin`"""
        return  [
            ('GDPFormatMenu', None, _('_Format'), None, None, None),
            ('RewrapText', None, _("Rewrap _text"), None,
                _("Rewrap the text to 78 characters."),
                formatter.rewrap_text),
            ('FixLineEnding', None, _("Fix _line endings"), None,
                _('Remove trailing whitespace and use newline endings.'),
                formatter.newline_ending),
            ('TabsToSpaces', None, _("Convert t_abs to spaces"), None,
                _('Convert tabs to spaces using the preferred tab size.'),
                formatter.tabs_to_spaces),
            ('QuoteLines', None, _("_Quote lines"), '<Alt>Q',
                _("Format the text as a quoted email."),
                formatter.quote_lines),
            ('SortImports', None, _("Sort _imports"), None,
                _('Sort and wrap imports.'),
                formatter.sort_imports),
            ('SingleLine', None, _("_Single line"), None,
                _("Format the text as a single line."),
                formatter.single_line),
            ('REReplace', None, _("Regular _expression line replace"), None,
                _("Reformat each line using a regular expression."),
                formatter.re_replace),
            ('ReformatDoctest', None, _("Reformat _doctest"), None,
                _("Reformat the doctest."),
                formatter.reformat_doctest),
            ('ReformatCSS', None, _("Reformat _CSS"), None,
                _("Reformat the CSS file or selection."),
                formatter.reformat_css),
            ('CheckProblems', None, _("C_heck syntax and style"), 'F3',
                _("Check syntax and style problems."),
                formatter.check_style),
            ('CheckAllProblems', None,
                _("Check syntax and style of all files"), None,
                _("Check syntax and style problems in all open documents."),
                formatter.check_all_style),
            ('ShowSyntaxErrorsOnly', None,
                _("Show syntax errors only"), None,
                _("Check syntax and style ignore info and warnings."),
                formatter.on_show_syntax_errors_only_toggled,
                config.getboolean('formatter', 'report_only_errors')),
            ]

    def __init__(self):
        """Initialize the plugin the whole Gedit application."""
        GObject.Object.__init__(self)
        self.controller = None

    def do_activate(self):
        """Activate the plugin in the current top-level window.

        Add 'Format' to the edit menu and create a Formatter.
        """
        self.activate()
        self.connect_signal(
            self.window, 'tab-added', self.on_tab_added_or_changed)
        self.connect_signal(
            self.window, 'active-tab-changed', self.on_tab_added_or_changed)

    def do_deactivate(self):
        """Deactivate the plugin in the current top-level window."""
        self.deactivate()

    def do_update_state(self):
        """Toggle the plugin's sensativity in the top-level window.

        This plugin is always active.
        """
        pass

    def on_tab_added_or_changed(self, window, tab):
        """Callback method for `tab-added` window signal.

        Connects `document-saved` signal.
        """
        document = tab.get_document()
        if self.controller is None:
            self.activate()
        self.controller.correct_language(document)
        language = document.get_language()
        if language is None:
            language_id = None
        else:
            language_id = language.get_id()
        manager = self.window.get_ui_manager()
        format_doctest_item = '/MenuBar/ToolsMenu/ToolsOps_2/ReformatDoctest'
        manager.get_action(format_doctest_item).props.sensitive = (
            language_id == 'doctest')
        format_css_item = '/MenuBar/ToolsMenu/ToolsOps_2/ReformatCSS'
        manager.get_action(format_css_item).props.sensitive = (
            language_id == 'css')
        self.connect_signal_after(
            document, 'syntax-error-python', self.controller.check_style)
        self.connect_signal_after(
            document, 'saved', self.controller.check_style_background)
