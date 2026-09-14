"""
AquaGuard - Dashboard Page

Dashboard widget displaying key monitoring statistics,
water quality status, alerts, and location summaries.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class DashboardPage(QWidget):
    """AquaGuard dashboard interface."""

    def __init__(self, analytics_engine):
        super().__init__()

        self.analytics = analytics_engine

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Build the dashboard interface."""

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Community water quality, consumption and conservation overview"
        )
        subtitle.setObjectName("PageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        cards_layout = QGridLayout()
        cards_layout.setSpacing(14)

        self.locations_card = self.create_card(
            "📍",
            "Locations",
            "0",
        )

        self.readings_card = self.create_card(
            "💧",
            "Water Readings",
            "0",
        )

        self.usage_card = self.create_card(
            "📊",
            "Average Usage",
            "0 L",
        )

        self.alerts_card = self.create_card(
            "⚠",
            "Active Alerts",
            "0",
        )

        cards_layout.addWidget(
            self.locations_card,
            0,
            0,
        )

        cards_layout.addWidget(
            self.readings_card,
            0,
            1,
        )

        cards_layout.addWidget(
            self.usage_card,
            0,
            2,
        )

        cards_layout.addWidget(
            self.alerts_card,
            0,
            3,
        )

        main_layout.addLayout(cards_layout)

        overview_layout = QHBoxLayout()
        overview_layout.setSpacing(15)

        quality_card = self.create_overview_card(
            "Water Quality",
        )

        self.quality_status = QLabel("No Data")
        self.quality_status.setObjectName("LargeStatus")

        self.quality_score = QLabel(
            "Quality Score: 0%"
        )

        self.quality_score.setObjectName("CardText")

        quality_card.layout().addWidget(
            self.quality_status
        )

        quality_card.layout().addWidget(
            self.quality_score
        )

        conservation_card = self.create_overview_card(
            "Water Conservation",
        )

        self.conservation_score = QLabel(
            "Conservation Score: 0%"
        )

        self.conservation_score.setObjectName(
            "CardText"
        )

        conservation_card.layout().addWidget(
            self.conservation_score
        )

        conservation_info = QLabel(
            "Higher scores indicate more readings "
            "within the configured consumption target."
        )

        conservation_info.setWordWrap(True)
        conservation_info.setObjectName(
            "CardText"
        )

        conservation_card.layout().addWidget(
            conservation_info
        )

        overview_layout.addWidget(
            quality_card
        )

        overview_layout.addWidget(
            conservation_card
        )

        main_layout.addLayout(
            overview_layout
        )

        summary_card = QFrame()
        summary_card.setObjectName("Card")

        summary_layout = QVBoxLayout(
            summary_card
        )

        summary_title = QLabel(
            "Location-wise Monitoring Summary"
        )

        summary_title.setObjectName(
            "CardTitle"
        )

        summary_layout.addWidget(
            summary_title
        )

        self.summary_table = QTableWidget()

        self.summary_table.setColumnCount(5)

        self.summary_table.setHorizontalHeaderLabels(
            [
                "Location",
                "Type",
                "Average Usage",
                "Quality",
                "Trend",
            ]
        )

        self.summary_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.summary_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self.summary_table.horizontalHeader().setStretchLastSection(
            True
        )

        summary_layout.addWidget(
            self.summary_table
        )

        main_layout.addWidget(
            summary_card,
            1,
        )

    def create_card(
        self,
        icon: str,
        title: str,
        value: str,
    ) -> QFrame:
        """Create a KPI card."""

        card = QFrame()
        card.setObjectName("KPICard")

        layout = QVBoxLayout(card)
        layout.setSpacing(5)

        icon_label = QLabel(icon)
        icon_label.setObjectName("KPIIcon")

        title_label = QLabel(title)
        title_label.setObjectName("KPITitle")

        value_label = QLabel(value)
        value_label.setObjectName("KPIValue")

        card.value_label = value_label

        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card

    def create_overview_card(
        self,
        title: str,
    ) -> QFrame:
        """Create an overview information card."""

        card = QFrame()
        card.setObjectName("Card")

        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setObjectName("CardTitle")

        layout.addWidget(title_label)
        layout.addSpacing(8)

        return card

    def refresh(self):
        """Refresh dashboard information."""

        if self.analytics is None:
            return

        summary = self.analytics.dashboard_summary()

        self.locations_card.value_label.setText(
            str(summary["locations"])
        )

        self.readings_card.value_label.setText(
            str(summary["readings"])
        )

        self.usage_card.value_label.setText(
            f'{summary["average_consumption"]:.1f} L'
        )

        self.alerts_card.value_label.setText(
            str(summary["active_alerts"])
        )

        self.quality_status.setText(
            f'● {summary["overall_quality"]}'
        )

        self.quality_score.setText(
            f'Quality Score: '
            f'{summary["quality_score"]}%'
        )

        self.conservation_score.setText(
            f'Conservation Score: '
            f'{summary["conservation_score"]}%'
        )

        self.refresh_summary_table()

    def refresh_summary_table(self):
        """Refresh the location summary table."""

        summaries = self.analytics.location_summary()

        self.summary_table.setRowCount(
            len(summaries)
        )

        for row, summary in enumerate(summaries):

            values = [
                summary["location"],
                summary["type"],
                f'{summary["average_consumption"]:.1f} L',
                summary["quality_status"],
                summary["trend"],
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.summary_table.setItem(
                    row,
                    column,
                    item,
                )
