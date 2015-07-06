# Created By: Virgil Dupras
# Created On: 2010-03-16
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QSizePolicy

class DateRangeSelectorView(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self._setupUi()

    def _setupUi(self):
        self.resize(259, 32)
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.prevButton = QPushButton(self)
        icon = QIcon()
        icon.addPixmap(QPixmap(":/nav_left_9"), QIcon.Normal, QIcon.Off)
        self.prevButton.setIcon(icon)
        self.horizontalLayout.addWidget(self.prevButton)
        self.typeButton = QPushButton("<date range>")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.typeButton.sizePolicy().hasHeightForWidth())
        self.typeButton.setSizePolicy(sizePolicy)
        self.typeButton.setMinimumSize(QSize(0, 0))
        self.typeButton.setMaximumSize(QSize(16777215, 16777215))
        self.typeButton.setIconSize(QSize(6, 6))
        self.horizontalLayout.addWidget(self.typeButton)
        self.nextButton = QPushButton(self)
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/nav_right_9"), QIcon.Normal, QIcon.Off)
        self.nextButton.setIcon(icon1)
        self.horizontalLayout.addWidget(self.nextButton)
        self.horizontalLayout.setStretch(1, 1)

