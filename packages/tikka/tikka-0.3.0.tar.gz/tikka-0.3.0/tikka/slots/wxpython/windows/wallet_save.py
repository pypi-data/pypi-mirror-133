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
from pathlib import Path
from typing import TYPE_CHECKING, TypeVar

import wx

from tikka.domains.application import Application
from tikka.domains.entities.account import Account
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.pubkey import PublicKey
from tikka.domains.interfaces.repository.preferences import (
    WALLET_SAVE_DEFAULT_DIRECTORY,
)
from tikka.libs.secret import generate_alphabetic
from tikka.slots.wxpython.entities.constants import (
    ARROW_RIGHT_IMAGE,
    HARD_DISK_IMAGE,
    KEYS_IMAGE,
)
from tikka.slots.wxpython.images import images

if TYPE_CHECKING or __name__ == "__main__":
    from tikka.slots.wxpython.windows.main import MainWindow

if TYPE_CHECKING:
    import _

MainWindowType = TypeVar("MainWindowType", bound="MainWindow")


class WalletSaveWindow(wx.Frame):
    def __init__(self, parent: MainWindowType, account: Account):
        """
        Init wallet save window

        :param parent: Instance of parent widget
        :param account: Account instance
        """
        super().__init__(parent)

        self.account = account

        self.SetTitle(
            _("Save wallet to disk")  # pylint: disable=used-before-assignment
        )

        default_font = self.GetFont()
        default_bold_font = default_font.Bold()

        # images
        keys_image = images.load(KEYS_IMAGE)
        keys_image.Rescale(200, 200, wx.IMAGE_QUALITY_HIGH)
        keys_icon = wx.StaticBitmap(self, -1, keys_image.ConvertToBitmap())

        arrow_right_image = images.load(ARROW_RIGHT_IMAGE)
        arrow_right_image.Rescale(200, 200, wx.IMAGE_QUALITY_HIGH)
        arrow_right_icon = wx.StaticBitmap(
            self, -1, arrow_right_image.ConvertToBitmap()
        )

        disk_image = images.load(HARD_DISK_IMAGE)
        disk_image.Rescale(200, 200, wx.IMAGE_QUALITY_HIGH)
        disk_icon = wx.StaticBitmap(self, -1, disk_image.ConvertToBitmap())

        # wallet file format
        wallet_format_label = wx.StaticText(self, label=_("Wallet file format"))
        wallet_format_label.SetFont(default_bold_font)
        # wait for dewif file format RFC
        # self.wallet_format_value = wx.Choice(self, choices=["DEWIF", "EWIF"])
        # self.wallet_format_value.SetSelection(0)
        self.wallet_format_value = wx.StaticText(self, label="EWIF")

        # public key label
        self.pubkey_label = wx.StaticText(self, label=_("Public key"))
        self.pubkey_label.SetFont(default_bold_font)
        self.pubkey_value = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.pubkey_value.SetMinSize((500, -1))
        self.pubkey_value.SetValue(str(PublicKey.from_pubkey(self.account.pubkey)))

        # browse
        self.browse_button = wx.Button(self, label=_("Browse disk..."))

        # access_code entry
        access_code_label = wx.StaticText(self, label=_("Access code"))
        access_code_label.SetFont(default_bold_font)
        self.access_code_value = wx.TextCtrl(self, style=wx.TE_READONLY)
        access_code_change_button = wx.Button(
            self,
            label=_("Change"),
        )
        self._generate_access_code()

        # error
        self.error_label = wx.StaticText(self, label=" ")
        self.error_label.SetForegroundColour("red")

        # layout
        images_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        images_sizer.Add(keys_icon)
        images_sizer.Add(arrow_right_icon)
        images_sizer.Add(disk_icon)

        access_code_sizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        access_code_sizer.Add(self.access_code_value)
        access_code_sizer.Add(access_code_change_button)

        form_sizer = wx.FlexGridSizer(rows=4, cols=2, hgap=5, vgap=5)
        form_sizer.Add(self.pubkey_label, flag=wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.pubkey_value)
        form_sizer.Add(wallet_format_label, flag=wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(self.wallet_format_value)
        form_sizer.Add(access_code_label, flag=wx.ALIGN_CENTER_VERTICAL)
        form_sizer.Add(access_code_sizer)

        sizer = wx.BoxSizer(orient=wx.VERTICAL)
        sizer.Add(images_sizer)
        sizer.Add(form_sizer, flag=wx.ALL | wx.EXPAND, border=10)
        sizer.Add(self.error_label, flag=wx.ALL | wx.ALIGN_CENTER, border=10)
        sizer.Add(self.browse_button, flag=wx.ALL | wx.ALIGN_CENTER, border=10)
        self.SetSizerAndFit(sizer)

        # events
        self.Bind(wx.EVT_BUTTON, lambda event: self._get_path(), self.browse_button)
        self.Bind(
            wx.EVT_BUTTON,
            lambda event: self._generate_access_code(),
            access_code_change_button,
        )

    def _generate_access_code(self):
        self.access_code_value.SetValue(generate_alphabetic())

    def _get_path(self):
        """
        Browse button event

        :return:
        """
        application_: Application = self.GetParent().application

        pubkey = PublicKey.from_pubkey_with_checksum(self.pubkey_value.GetValue())
        # extension = self.wallet_format_value.GetString(
        #     self.wallet_format_value.GetSelection()
        # ).lower()
        extension = self.wallet_format_value.GetLabel().lower()
        if extension == "ewif":
            extension = "dunikey"
        filename = "{name}_{pubkey}-{checksum}_{currency}.{extension}".format(  # pylint: disable=consider-using-f-string
            name=_("Wallet"),
            pubkey=pubkey.shorten,
            checksum=pubkey.checksum,
            currency=application_.config.get("currency"),
            extension=extension,
        )

        default_dir = application_.preferences_repository.get(
            WALLET_SAVE_DEFAULT_DIRECTORY
        )
        if default_dir is not None:
            default_dir = str(Path(default_dir).expanduser().absolute())
        else:
            default_dir = ""

        with wx.FileDialog(
            self,
            _("Save wallet to disk"),
            defaultDir=default_dir,
            wildcard=_("All files (*.*)|*.*|EWIF files (*.dunikey)|*.dunikey"),
            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
            defaultFile=filename,
        ) as file_dialog:
            if file_dialog.ShowModal() == wx.ID_CANCEL:
                # close window
                self.Close()
                return  # the user changed their mind

            # Get the file path chosen by the user
            pathname = file_dialog.GetPath()

        # update default dir preference
        application_.preferences_repository.set(
            WALLET_SAVE_DEFAULT_DIRECTORY,
            str(Path(pathname).expanduser().absolute().parent),
        )

        # application save wallet
        result = self.GetParent().application.accounts.save_wallet(
            self.account,
            pathname,
            self.access_code_value.GetValue(),
            self.GetParent().application.config.get("currency"),
        )
        if not result:
            self.error_label.SetLabel(_("Failed to save wallet!"))
            self.GetSizer().Layout()
            return

        # GUI save wallet
        self.GetParent().save_wallet(self.account)
        # close window
        self.Close()


if __name__ == "__main__":
    # create gui application
    wx_app = wx.App()
    # create domain application
    application = Application(DATA_PATH)
    # create gui
    main_window = MainWindow(None, application)
    _account = Account("H5RS687NT622b9LWyjdtR8BuHrAdREn3y5XpuYWkzAMk")
    WalletSaveWindow(main_window, _account).Show()

    # start gui event loop
    wx_app.MainLoop()
