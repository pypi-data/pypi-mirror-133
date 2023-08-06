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
from wx.aui import AuiNotebook

from tikka.domains.entities.account import Account
from tikka.slots.wxpython.entities.constants import (
    LOCKED_IMAGE,
    SAFE_IMAGE,
    UNLOCKED_IMAGE,
)
from tikka.slots.wxpython.images import images
from tikka.slots.wxpython.menus.account_popup import AccountPopupMenu


class AccountPanel(wx.Panel):
    def __init__(self, parent: AuiNotebook, account: Account):
        """
        Init account tab frame


        :param parent: Parent Notebook
        :param account: Account instance
        """
        super().__init__(parent)

        self.id = account.pubkey

        safe_image = images.load(SAFE_IMAGE)
        safe_image.Rescale(100, 100, wx.IMAGE_QUALITY_HIGH)
        safe_icon = wx.StaticBitmap(self, -1, safe_image.ConvertToBitmap())

        self.balance = wx.StaticText(self, label="0")
        balance_font = self.balance.GetFont().Bold().Scale(4)
        self.balance.SetFont(balance_font)

        locked_image = images.load(LOCKED_IMAGE)
        locked_image.Rescale(50, 50, wx.IMAGE_QUALITY_HIGH)
        self.locked_bitmap = locked_image.ConvertToBitmap()
        unlocked_image = images.load(UNLOCKED_IMAGE)
        unlocked_image.Rescale(50, 50, wx.IMAGE_QUALITY_HIGH)
        self.unlocked_bitmap = unlocked_image.ConvertToBitmap()
        self.locked_status_icon = wx.StaticBitmap(self, -1, self.locked_bitmap)

        self.set_unlock_status(account)

        self.pubkey = wx.StaticText(self, label=account.pubkey)
        pubkey_font = self.pubkey.GetFont().Bold()
        self.pubkey.SetFont(pubkey_font)

        # layout
        self.grid_sizer = wx.GridBagSizer(vgap=10, hgap=10)
        self.grid_sizer.Add(safe_icon, pos=(0, 0), flag=wx.ALIGN_CENTER, border=10)
        self.grid_sizer.Add(
            self.balance,
            pos=(0, 1),
            flag=wx.TOP | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=10,
        )
        self.grid_sizer.Add(
            self.locked_status_icon, pos=(1, 0), flag=wx.ALIGN_CENTER, border=10
        )
        self.grid_sizer.Add(
            self.pubkey,
            pos=(1, 1),
            flag=wx.TOP | wx.ALIGN_CENTER_VERTICAL | wx.EXPAND,
            border=10,
        )

        self.SetSizer(self.grid_sizer)

        # events
        safe_icon.Bind(wx.EVT_RIGHT_DOWN, lambda event: self._right_click())
        self.balance.Bind(
            wx.EVT_RIGHT_DOWN,
            lambda event: self._right_click(),
        )
        self.locked_status_icon.Bind(
            wx.EVT_RIGHT_DOWN,
            lambda event: self._right_click(),
            self.locked_status_icon,
        )
        self.pubkey.Bind(wx.EVT_RIGHT_DOWN, lambda event: self._right_click())
        self.Bind(wx.EVT_RIGHT_DOWN, lambda event: self._right_click())

    def _right_click(self) -> None:
        """
        Display popup menu on listbox

        :return:
        """
        account = self.GetGrandParent().application.accounts.get_by_pubkey(self.id)
        if account is None:
            return None
        # create popup menu
        popup_menu = AccountPopupMenu(
            self.GetGrandParent(),
            account,
        )

        # show popup menu
        self.PopupMenu(popup_menu)

        return None

    def update(self, account: Account):
        """
        Set account to display

        :param account: Account instance
        :return:
        """
        self.balance.SetLabel("0")
        self.set_unlock_status(account)

        self.Layout()

    def set_unlock_status(self, account: Account):
        """
        Set access status in display from account

        :param account: Account instance
        :return:
        """
        self.locked_status_icon.SetBitmap(
            self.locked_bitmap if account.signing_key is None else self.unlocked_bitmap
        )
        self.locked_status_icon.Layout()


if __name__ == "__main__":

    class AccountsMock:
        list = [Account("732SSfuwjB7jkt9th1zerGhphs6nknaCBCTozxUcPWPU")]

    class Application(wx.App):
        def __init__(self):
            super().__init__()
            self.accounts = AccountsMock()

    class MockMainWindow(wx.Frame):
        def __init__(self, parent, application=None):
            super().__init__(parent)
            self.application = application

    wx_app = Application()

    main_window_ = MockMainWindow(None, application=wx_app)
    notebook = AuiNotebook(main_window_)
    account_panel1 = AccountPanel(notebook, wx_app.accounts.list[0])
    account_panel2 = AccountPanel(notebook, wx_app.accounts.list[0])
    account_panel3 = AccountPanel(notebook, wx_app.accounts.list[0])
    notebook.AddPage(account_panel1, "Account 1")
    notebook.AddPage(account_panel2, "Account 2")
    notebook.AddPage(account_panel3, "Account 3")
    main_window_.SetClientSize(notebook.GetBestSize())
    main_window_.Show()

    wx_app.MainLoop()
