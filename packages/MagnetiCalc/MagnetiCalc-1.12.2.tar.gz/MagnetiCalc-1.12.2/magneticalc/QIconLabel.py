""" QIconLabel module. """

#  ISC License
#
#  Copyright (c) 2020–2022, Paul Wilhelm, M. Sc. <anfrage@paulwilhelm.de>
#
#  Permission to use, copy, modify, and/or distribute this software for any
#  purpose with or without fee is hereby granted, provided that the above
#  copyright notice and this permission notice appear in all copies.
#
#  THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
#  WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
#  MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
#  ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
#  WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
#  ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
#  OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

from typing import Optional
from PyQt5.Qt import QFont
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QHBoxLayout
from magneticalc.QLabel2 import QLabel2
from magneticalc.Theme import Theme


class QIconLabel(QHBoxLayout):
    """ QIconLabel class. """

    # Default spacing
    HorizontalSpacing = 1

    def __init__(
            self,
            text: str,
            icon: str,
            text_color: str = Theme.DarkColor,
            icon_color: str = Theme.DarkColor,
            icon_size: QSize = QSize(16, 16),
            font: Optional[QFont] = None,
            expand: bool = True
    ) -> None:
        """
        Initializes the icon label.

        @param text: Label text
        @param icon: QtAwesome icon id
        @param text_color: Text color
        @param icon_color: Icon color
        @param icon_size: Icon size
        @param font: QFont
        @param expand: Enable to expand label
        """
        QHBoxLayout.__init__(self)
        self.setContentsMargins(0, 0, 0, 0)

        if icon != "":
            self.addWidget(QLabel2("", icon=icon, icon_color=icon_color, icon_size=icon_size, expand=False))
            self.addSpacing(self.HorizontalSpacing)

        self.addWidget(QLabel2(text, font=font, bold=True, color=text_color, expand=expand))
