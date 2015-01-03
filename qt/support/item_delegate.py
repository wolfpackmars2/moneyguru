# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2010-01-07
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

from collections import namedtuple

from PyQt4.QtCore import QRect, QSize
from PyQt4.QtGui import QStyledItemDelegate, QStyleOptionViewItemV4, QStyle

# onClickCallable has the signature f(clicked_row_index: int).
ItemDecoration = namedtuple('ItemDecoration', 'pixmap onClickCallable')

class ItemDelegate(QStyledItemDelegate):

    def __init__(self, *args, **kwargs):
        QStyledItemDelegate.__init__(self, *args, **kwargs)
        self._display_text = True

    #--- Virtual
    def _get_decorations(self, index, isSelected):
        """Returns a list of ItemDecorations which are drawn during the paint event.

        The list returned of instances of ItemDecoration will be drawn in the appropriate
        field.  If the decorations should perform a function, the second value of the
        tuple (onClickCallable property) should be set to an argument-less function.

        Args:
            index - QModelIndex

        Returns:
            List of instances of ItemDecoration

        """
        # Must return a list of ItemDecoration for each little image you want to put at the right
        # side of the cell. If you want them to be clickable, set onClickCallable with an argument-
        # less function.
        return []

    def _get_value_painter(self, index):
        """Returns a value painter used to paint the data contained at the index.

        Returns an instance of an object that will be used to do custom painting of the
        value of the data within the model at the specified index.  This object should
        have a paint and sizeHint method in order to determine the size required to paint
        the value and a method to do that painting.

        Args:
            index - QModelIndex

        Returns:
            An object that has a paint and sizeHint method.

        """
        return None

    def _prepare_paint_options(self, option, index):
        # Don't set option directly in `paint` but here. This way, there won't be any trouble with
        # option being overwritten.
        pass

    #--- Overrides

    def displayText(self, p_object, locale):
        if self._display_text:
            return QStyledItemDelegate.displayText(self, p_object, locale)
        return ""

    def sizeHint(self, option, index):
        """Returns a QSize bounding box of the area required to paint the data in the model at the index.

        Returns the size of the bounding box of the area required to paint the data in the model
        at the specified index.  This is the sum of decoration pixmap widths, and the sizeHint provided
        by the custom value_painter if it exists.

        Args:
            option - QStyleOptionViewItemV4
            index - QModelIndex

        Returns:
            A QSize bounding box of the size required to paint the value of the data in the model plus
            decorations.

        """
        value_painter = self._get_value_painter(index)
        if value_painter is None:
            return QStyledItemDelegate.sizeHint(self, option, index)
        decs = self._get_decorations(index, bool(option.state & QStyle.State_Selected))
        pix_widths = [dec.pixmap.width() for dec in decs]
        size = value_painter.sizeHint(option, index)
        size.setWidth(size.width() + sum(pix_widths))
        return size

    def handleClick(self, index, pos, itemRect, selected):
        # Returns True if at one of the decorations were in the hit zone.
        decorations = self._get_decorations(index, selected)
        currentRight = itemRect.right()
        for dec in decorations:
            pixmap = dec.pixmap
            if pos.x() >= currentRight - pixmap.width():
                dec.onClickCallable(index)
                return True
            currentRight -= pixmap.width()
        return False

    def paint(self, painter, option, index):
        """Performs custom painting of value of data in the model and decorations.

         Performs custom painting of value of data in the model at the specified index
         plus any decorations used in that column.

         Args:
            painter - QPainter
            option - QStyleOptionViewItemV4
            index - QModelIndex
        """
        self.initStyleOption(option, index)
        # I don't know why I have to do this. option.version returns 4, but still, when I try to
        # access option.features, boom-crash. The workaround is to force a V4.
        option = QStyleOptionViewItemV4(option)
        decorations = self._get_decorations(index, bool(option.state & QStyle.State_Selected))
        if decorations:
            option.decorationPosition = QStyleOptionViewItemV4.Right
            decorationWidth = sum(dec.pixmap.width() for dec in decorations)
            decorationHeight = max(dec.pixmap.height() for dec in decorations)
            option.decorationSize = QSize(decorationWidth, decorationHeight)
            option.features |= QStyleOptionViewItemV4.HasDecoration
        self._prepare_paint_options(option, index)

        xOffset = 0
        # First added for #15, the painting of custom amount information.  This can
        # be used as a pattern for painting any column of information.
        value_painter = self._get_value_painter(index)
        self._display_text = value_painter is None
        QStyledItemDelegate.paint(self, painter, option, index)
        if value_painter is not None:
            value_option = QStyleOptionViewItemV4(option)
            rect = value_option.rect
            rect = QRect(rect.left(), rect.top(), rect.width() - xOffset, rect.height())
            value_option.rect = rect
            value_painter.paint(painter, value_option, index)

        for dec in decorations:
            pixmap = dec.pixmap
            x = option.rect.right() - pixmap.width() - xOffset
            y = option.rect.center().y() - (pixmap.height() // 2)
            rect = QRect(x, y, pixmap.width(), pixmap.height())
            painter.drawPixmap(rect, pixmap)
            xOffset += pixmap.width()

    def setModelData(self, editor, model, index):
        # This call below is to give a chance to the editor to tweak its content a little bit before
        # we send it to the model.
        if hasattr(editor, 'prepareDataForCommit'):
            editor.prepareDataForCommit()
        QStyledItemDelegate.setModelData(self, editor, model, index)

