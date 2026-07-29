"""
AstroAlign
Overlay graphics item.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QGraphicsItem,
    QGraphicsPixmapItem,
)


class OverlayItem(QGraphicsPixmapItem):
    """
    Interactive Stellarium overlay.
    Responsible for all overlay transformations.
    """

    MIN_SCALE = 0.05
    MAX_SCALE = 20.0

    def __init__(self, pixmap: QPixmap):

        super().__init__(pixmap)

        self.rotation_angle = 0.0
        self.scale_factor = 1.0

        self.setOpacity(0.50)
        self.setZValue(10)

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

        #
        # Rotate and scale about the centre of the image.
        #

        self.setTransformOriginPoint(
            self.boundingRect().center()
        )

    # -------------------------------------------------
    # Rotation
    # -------------------------------------------------

    def rotate(self, delta_degrees: float):

        self.rotation_angle += delta_degrees
        self.setRotation(self.rotation_angle)

    # -------------------------------------------------
    # Scaling
    # -------------------------------------------------

    def scale_by(self, factor: float):

        new_scale = self.scale_factor * factor

        new_scale = max(
            self.MIN_SCALE,
            min(self.MAX_SCALE, new_scale)
        )

        self.scale_factor = new_scale

        self.setScale(self.scale_factor)

    # -------------------------------------------------
    # Opacity
    # -------------------------------------------------

    def set_overlay_opacity(self, opacity: float):

        opacity = max(0.0, min(1.0, opacity))
        self.setOpacity(opacity)

    # -------------------------------------------------
    # Reset
    # -------------------------------------------------

    def reset_transformations(self):

        self.rotation_angle = 0.0
        self.scale_factor = 1.0

        self.setRotation(0.0)
        self.setScale(1.0)