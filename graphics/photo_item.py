"""
AstroAlign
Image viewer.
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QKeyEvent, QPainter, QPixmap
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

        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.setTransformationAnchor(
            QGraphicsView.AnchorUnderMouse
        )

        self.setResizeAnchor(
            QGraphicsView.AnchorViewCenter
        )

        self.setDragMode(
            QGraphicsView.ScrollHandDrag
        )

        # Important so the widget receives keyboard events.
        self.setFocusPolicy(Qt.StrongFocus)

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

        self.status_changed.emit(
            "Photograph loaded."
        )

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

        if self.overlay_item is not None:
            self.scene.removeItem(
                self.overlay_item
            )

        self.overlay_item = OverlayItem(pixmap)

        #
        # Centre the overlay on the photograph
        #

        photo_rect = self.photo_item.boundingRect()
        overlay_rect = self.overlay_item.boundingRect()

        x = (
            photo_rect.center().x()
            - overlay_rect.width() / 2
        )

        y = (
            photo_rect.center().y()
            - overlay_rect.height() / 2
        )

        self.overlay_item.setPos(x, y)

        self.scene.addItem(
            self.overlay_item
        )

        self.overlay_item.setSelected(True)

        self.setFocus()

        self.status_changed.emit(
            "Overlay loaded. "
            "Q/E rotate   +/- scale"
        )

    # --------------------------------------------------

    def remove_overlay(self):

        if self.overlay_item:

            self.scene.removeItem(
                self.overlay_item
            )

            self.overlay_item = None

            self.status_changed.emit(
                "Overlay removed."
            )

    # --------------------------------------------------

    def fit_to_window(self):

        if self.photo_item is None:
            return

        self.fitInView(
            self.photo_item,
            Qt.KeepAspectRatio,
        )

        self.zoom_factor = 1.0

        self.status_changed.emit(
            "Fit to window."
        )

    # --------------------------------------------------

    def reset_zoom(self):

        self.resetTransform()

        self.zoom_factor = 1.0

        self.status_changed.emit(
            "100% zoom."
        )

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

    def keyPressEvent(
        self,
        event: QKeyEvent,
    ):

        if self.overlay_item is None:
            super().keyPressEvent(event)
            return

        key = event.key()

        if key == Qt.Key_Q:

            self.overlay_item.rotate_left()

            self.status_changed.emit(
                f"Rotation : "
                f"{self.overlay_item.rotation_angle:.1f}°"
            )

            return

        if key == Qt.Key_E:

            self.overlay_item.rotate_right()

            self.status_changed.emit(
                f"Rotation : "
                f"{self.overlay_item.rotation_angle:.1f}°"
            )

            return

        if key in (
            Qt.Key_Plus,
            Qt.Key_Equal,
        ):

            self.overlay_item.scale_up()

            self.status_changed.emit(
                f"Scale : "
                f"{self.overlay_item.scale_factor:.2f}"
            )

            return

        if key == Qt.Key_Minus:

            self.overlay_item.scale_down()

            self.status_changed.emit(
                f"Scale : "
                f"{self.overlay_item.scale_factor:.2f}"
            )

            return

        super().keyPressEvent(event)

    # --------------------------------------------------

    def mouseMoveEvent(self, event):

        point = self.mapToScene(event.pos())

        self.status_changed.emit(

            f"X: {point.x():.0f}    "
            f"Y: {point.y():.0f}    "
            f"Zoom: {self.zoom_factor:.2f}"

        )

        super().mouseMoveEvent(event)