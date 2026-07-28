"""
AstroAlign
Main application window.
"""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QToolBar,
)

from ui.image_view import ImageView


class MainWindow(QMainWindow):
    """
    Main application window.
    """

    def __init__(self) -> None:

        super().__init__()

        self.setWindowTitle("AstroAlign v0.3.0")
        self.resize(1600, 900)

        self.image_view = ImageView()
        self.setCentralWidget(self.image_view)

        self._create_toolbar()
        self._create_statusbar()

    # ---------------------------------------------------------
    # Toolbar
    # ---------------------------------------------------------

    def _create_toolbar(self) -> None:

        toolbar = QToolBar("Main")
        toolbar.setMovable(False)

        self.addToolBar(Qt.TopToolBarArea, toolbar)

        action = QAction("Open Photo", self)
        action.triggered.connect(self.open_photo)
        toolbar.addAction(action)

        action = QAction("Open Overlay", self)
        action.triggered.connect(self.open_overlay)
        toolbar.addAction(action)

        action = QAction("Remove Overlay", self)
        action.triggered.connect(self.image_view.remove_overlay)
        toolbar.addAction(action)

        toolbar.addSeparator()

        action = QAction("Fit", self)
        action.triggered.connect(self.image_view.fit_to_window)
        toolbar.addAction(action)

        action = QAction("100%", self)
        action.triggered.connect(self.image_view.reset_zoom)
        toolbar.addAction(action)

    # ---------------------------------------------------------
    # Status Bar
    # ---------------------------------------------------------

    def _create_statusbar(self) -> None:

        status = QStatusBar()

        self.setStatusBar(status)

        self.lbl_status = QLabel("Ready")

        status.addPermanentWidget(self.lbl_status)

        self.image_view.status_changed.connect(
            self.lbl_status.setText
        )

    # ---------------------------------------------------------
    # Open photograph
    # ---------------------------------------------------------

    def open_photo(self) -> None:

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Photograph",
            str(Path.home()),
            (
                "Images (*.jpg *.jpeg *.png "
                "*.bmp *.tif *.tiff)"
            ),
        )

        if not filename:
            return

        try:

            self.image_view.load_photo(filename)

        except Exception as ex:

            QMessageBox.critical(
                self,
                "Error",
                str(ex),
            )

    # ---------------------------------------------------------
    # Open Stellarium overlay
    # ---------------------------------------------------------

    def open_overlay(self) -> None:

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Stellarium Overlay",
            str(Path.home()),
            (
                "Images (*.jpg *.jpeg *.png)"
            ),
        )

        if not filename:
            return

        try:

            self.image_view.load_overlay(filename)

        except Exception as ex:

            QMessageBox.critical(
                self,
                "Error",
                str(ex),
            )