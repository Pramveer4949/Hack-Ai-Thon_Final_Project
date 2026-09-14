"""
AquaGuard
Community Water Quality & Usage Monitor

Main application entry point.

Theme:
    Python Fundamentals + Object-Oriented Programming (OOP)
    Sustainable Development Goals (SDG 6 and SDG 12)

This file starts the AquaGuard desktop application.
"""

import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import AquaGuardWindow


def main():
    """Start the AquaGuard application."""

    app = QApplication(sys.argv)

    app.setApplicationName("AquaGuard")
    app.setOrganizationName("AquaGuard")
    app.setApplicationVersion("1.0.0")

    window = AquaGuardWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
