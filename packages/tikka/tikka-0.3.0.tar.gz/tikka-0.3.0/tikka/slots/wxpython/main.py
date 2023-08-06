#!/usr/bin/env python3

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
import wx

from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.interfaces.main import MainApplicationInterface
from tikka.slots.wxpython.windows.main import MainWindow


class WxPythonMainApplication(MainApplicationInterface):
    """
    WxPythonMainApplication class
    """

    def __init__(
        self, application: Application
    ):  # pylint: disable=super-init-not-called
        __doc__ = (  # pylint: disable=redefined-builtin, unused-variable
            MainApplicationInterface.__init__.__doc__
        )
        # create wx.App
        wx_app = wx.App()

        # create wx main window gui
        gui = MainWindow(None, application)
        gui.Show()

        # start wx event loop
        wx_app.MainLoop()


if __name__ == "__main__":
    # create domain application
    application_ = Application(DATA_PATH)
    # init main application
    WxPythonMainApplication(application_)
