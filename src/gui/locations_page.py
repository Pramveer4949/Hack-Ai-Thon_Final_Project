"""
AquaGuard - Locations Page

Manage and view monitored households, schools,
and community water-monitoring locations.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class LocationsPage(QWidget):
    """Page for viewing monitored locations."""

    def __init__(self, database):
        super().__init__()

        self.database = database

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Build the locations interface."""

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        main_layout.setSpacing(18)

        title = QLabel("Locations")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Manage households, schools, and community monitoring locations"
        )

        subtitle.setObjectName("PageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        summary_card = QFrame()
        summary_card.setObjectName("Card")

        summary_layout = QHBoxLayout(
            summary_card
        )

        self.count_label = QLabel(
            "0 Monitoring Locations"
        )

        self.count_label.setObjectName(
            "LargeStatus"
        )

        summary_layout.addWidget(
            self.count_label
        )

        summary_layout.addStretch()

        refresh_button = QPushButton(
            "↻ Refresh"
        )

        refresh_button.clicked.connect(
            self.refresh
        )

        summary_layout.addWidget(
            refresh_button
        )

        main_layout.addWidget(
            summary_card
        )

        table_card = QFrame()
        table_card.setObjectName("Card")

        table_layout = QVBoxLayout(
            table_card
        )

        table_title = QLabel(
            "Registered Monitoring Locations"
        )

        table_title.setObjectName(
            "CardTitle"
        )

        table_layout.addWidget(
            table_title
        )

        self.location_table = QTableWidget()

        self.location_table.setColumnCount(
            5
        )

        self.location_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Location",
                "Type",
                "Responsible Person",
                "Daily Target",
            ]
        )

        self.location_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.location_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.location_table.horizontalHeader().setStretchLastSection(
            True
        )

        table_layout.addWidget(
            self.location_table
        )

        main_layout.addWidget(
            table_card,
            1,
        )

    def refresh(self):
        """Refresh the registered locations."""

        locations = self.database.get_locations()

        self.count_label.setText(
            f"{len(locations)} Monitoring Locations"
        )

        self.location_table.setRowCount(
            len(locations)
        )

        for row, location in enumerate(
            locations
        ):

            values = [
                location.location_id,
                location.name,
                location.location_type,
                location.responsible_person,
                f"{location.target_daily_liters:.1f} L",
            ]

            for column, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.location_table.setItem(
                    row,
                    column,
                    item
                )

        self.location_table.resizeRowsToContents()

    def refresh_locations(self):
        """Compatibility method for the main window."""

        self.refresh()
