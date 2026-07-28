"""
AstroAlign
Image viewer.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPainter, QPixmap
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
)

from graphics.overlay_item import OverlayItem
from graphics.photo_item import PhotoItem


class ImageView(QGraphicsView):

    status_changed = Signal(str)

    def __init__(self):

        super().__init__()

        self.scene = QGraphicsScene(self)

        self.setScene(self.scene)

        self.setRenderHint(
            QPainter.Antialiasing,
            True,
        )

        self.setRenderHint(
            QPainter.SmoothPixmapTransform,
            True,
        )

        self.setTransformationAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.AnchorViewCenter
        )

        self.setDragMode(
            QGraphicsView.ScrollHandDrag
        )

        self.photo_item = None
        self.overlay_item = None

        self.zoom_factor = 1.0

    # --------------------------------------------------

    def load_photo(self, filename: str):

        image = QImage(filename)

        if image.isNull():

            raise RuntimeError(
                "Unable to load image."
            )

        pixmap = QPixmap.fromImage(image)

        self.scene.clear()

        self.photo_item = PhotoItem(pixmap)

        self.scene.addItem(self.photo_item)

        self.overlay_item = None

        self.setSceneRect(
            self.photo_item.boundingRect()
        )

        self.fit_to_window()

    # --------------------------------------------------

    def load_overlay(self, filename: str):

        if self.photo_item is None:

            return

        image = QImage(filename)

        if image.isNull():

            raise RuntimeError(
                "Unable to load overlay."
            )

        pixmap = QPixmap.fromImage(image)

        if self.overlay_item:

            self.scene.removeItem(
                self.overlay_item
            )

        self.overlay_item = OverlayItem(
            pixmap
        )

        self.scene.addItem(
            self.overlay_item
        )

    # --------------------------------------------------

    def remove_overlay(self):

        if self.overlay_item:

            self.scene.removeItem(
                self.overlay_item
            )

            self.overlay_item = None

    # --------------------------------------------------

    def fit_to_window(self):

        if self.photo_item is None:

            return

        self.fitInView(
            self.photo_item,
            Qt.KeepAspectRatio,
        )

        self.zoom_factor = 1.0

    # --------------------------------------------------

    def reset_zoom(self):

        self.resetTransform()

        self.zoom_factor = 1.0

    # --------------------------------------------------

    def wheelEvent(self, event):

        factor = 1.15

        if event.angleDelta().y() > 0:

            self.scale(
                factor,
                factor,
            )

            self.zoom_factor *= factor

        else:

            self.scale(
                1 / factor,
                1 / factor,
            )

            self.zoom_factor /= factor

        self.status_changed.emit(
            f"Zoom : {self.zoom_factor:.2f}x"
        )

    # --------------------------------------------------

    def mouseMoveEvent(self, event):

        point = self.mapToScene(event.pos())

        self.status_changed.emit(

            f"X: {point.x():.0f}    "
            f"Y: {point.y():.0f}    "
            f"Zoom: {self.zoom_factor:.2f}"

        )

        super().mouseMoveEvent(event)