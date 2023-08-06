# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import builtins
from typing import TYPE_CHECKING, List

import markdown
import wx
from wx.aui import AuiNotebook
from wx.html import HtmlWindow

from tikka.domains.entities.constants import LOCALES_PATH
from tikka.slots.wxpython.entities.constants import LICENCE_TAB_ID

if TYPE_CHECKING:
    import _

builtins.__dict__["_"] = wx.GetTranslation


class LicencePanel(wx.Panel):
    def __init__(self, parent: AuiNotebook, language: str):
        """
        Init licence panel

        :param parent: Instance of parent notebook
        :param language: Language config code
        """
        super().__init__(parent)

        self.id = LICENCE_TAB_ID

        with open(
            LOCALES_PATH.joinpath(language, "licence_g1.txt"),
            "r",
            encoding="utf-8",
        ) as input_file:
            text = input_file.read()
        html = markdown.markdown(text)

        html_display = HtmlWindow(self)
        html_display.SetPage(html)

        sizer = wx.BoxSizer()
        sizer.Add(html_display, 1, wx.EXPAND)

        self.SetSizer(sizer)


if __name__ == "__main__":

    wx_app = wx.App()

    class AccountsMock:
        list: List = []

    class Application:
        def __init__(self):
            super().__init__()
            self.accounts = AccountsMock()

    class MockMainWindow(wx.Frame):
        def __init__(self, parent, application=None):
            super().__init__(parent)
            self.application = application
            self.notebook = AuiNotebook(self)

    application_ = Application()

    main_window = MockMainWindow(None, application=application_)

    licence_panel = LicencePanel(main_window.notebook, "fr_FR")
    main_window.notebook.AddPage(
        licence_panel, _("Ğ1 licence")  # pylint: disable=used-before-assignment
    )
    main_window.Show()

    wx_app.MainLoop()
