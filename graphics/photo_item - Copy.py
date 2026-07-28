"""
AstroAlign
Photo graphics item.
"""

from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsPixmapItem


class PhotoItem(QGraphicsPixmapItem):
    """
    Graphics item representing the user's photograph.
    """

    def __init__(self, pixmap: QPixmap):

        super().__init__(pixmap)

        self.setZValue(0)