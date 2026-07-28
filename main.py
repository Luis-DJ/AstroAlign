"""
AstroAlign
Version 0.3.0

Application entry point.
"""

import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow


def main() -> int:
    """
    Application entry point.
    """

    app = QApplication(sys.argv)

    app.setApplicationName("AstroAlign")
    app.setApplicationVersion("0.3.0")

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())