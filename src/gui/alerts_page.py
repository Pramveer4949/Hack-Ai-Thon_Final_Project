"""
AquaGuard - Alerts Page

Displays unsafe water-quality readings and excessive
water-consumption alerts.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class AlertsPage(QWidget):
    """Page for viewing water-monitoring alerts."""

    def __init__(self, analytics_engine):
        super().__init__()

        self.analytics = analytics_engine

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Build the alerts interface."""

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        main_layout.setSpacing(18)

        title = QLabel("Alerts & Recommendations")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Review abnormal water readings and recommended actions"
        )

        subtitle.setObjectName("PageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        summary_card = QFrame()
        summary_card.setObjectName("Card")

        summary_layout = QHBoxLayout(
            summary_card
        )

        self.alert_count_label = QLabel(
            "0 Active Alerts"
        )

        self.alert_count_label.setObjectName(
            "LargeStatus"
        )

        summary_layout.addWidget(
            self.alert_count_label
        )

        summary_layout.addStretch()

        information = QLabel(
            "Alerts are generated using the configured "
            "water-quality and consumption thresholds."
        )

        information.setWordWrap(True)
        information.setObjectName("CardText")

        summary_layout.addWidget(
            information
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
            "Active Monitoring Alerts"
        )

        table_title.setObjectName(
            "CardTitle"
        )

        table_layout.addWidget(
            table_title
        )

        self.alert_table = QTableWidget()

        self.alert_table.setColumnCount(
            6
        )

        self.alert_table.setHorizontalHeaderLabels(
            [
                "Date",
                "Location",
                "Parameter",
                "Value",
                "Severity",
                "Recommended Action",
            ]
        )

        self.alert_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.alert_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.alert_table.setWordWrap(True)

        self.alert_table.horizontalHeader().setStretchLastSection(
            True
        )

        table_layout.addWidget(
            self.alert_table
        )

        main_layout.addWidget(
            table_card,
            1,
        )

    def refresh(self):
        """Refresh the alert list."""

        alerts = self.analytics.get_alerts()

        self.alert_count_label.setText(
            f"{len(alerts)} Active Alerts"
        )

        self.alert_table.setRowCount(
            len(alerts)
        )

        for row, alert in enumerate(alerts):

            values = [
                alert["date"],
                alert["location"],
                alert["parameter"],
                alert["value"],
                alert["severity"],
                alert["recommendation"],
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

                item.setToolTip(
                    str(value)
                )

                self.alert_table.setItem(
                    row,
                    column,
                    item
                )

        self.alert_table.resizeRowsToContents()

    def refresh_alerts(self):
        """Compatibility method for the main window."""

        self.refresh()
