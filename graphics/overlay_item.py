"""
AstroAlign
Overlay graphics item.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsItem, QGraphicsPixmapItem


class OverlayItem(QGraphicsPixmapItem):
    """
    Graphics item representing the Stellarium overlay.
    """

    def __init__(self, pixmap: QPixmap):

        super().__init__(pixmap)

        self.setZValue(10)

        self.setOpacity(0.50)

        self.setFlag(
            QGraphicsItem.ItemIsMovable,
            True,
        )

        self.setFlag(
            QGraphicsItem.ItemIsSelectable,
            True,
        )

        self.setTransformationMode(
            Qt.SmoothTransformation
        )

        self.setTransformOriginPoint(
            self.boundingRect().center()
        )

        self.rotation_angle = 0.0
        self.scale_factor = 1.0

    # --------------------------------------------------

    def rotate_left(self, degrees: float = 1.0):

        self.rotation_angle -= degrees
        self.setRotation(self.rotation_angle)

    # --------------------------------------------------

    def rotate_right(self, degrees: float = 1.0):

        self.rotation_angle += degrees
        self.setRotation(self.rotation_angle)

    # --------------------------------------------------

    def scale_up(self, amount: float = 0.02):

        self.scale_factor += amount
        self.setScale(self.scale_factor)

    # --------------------------------------------------

    def scale_down(self, amount: float = 0.02):

        self.scale_factor = max(
            0.05,
            self.scale_factor - amount,
        )

        self.setScale(self.scale_factor)