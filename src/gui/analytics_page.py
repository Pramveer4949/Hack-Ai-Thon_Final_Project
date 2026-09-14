"""
AquaGuard - Analytics Page

Provides visual analysis of water consumption,
water quality, trends, and location performance.
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

try:
    from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
    from matplotlib.figure import Figure
except ImportError:
    FigureCanvasQTAgg = None
    Figure = None


class AnalyticsPage(QWidget):
    """Analytics and trend visualization page."""

    def __init__(self, analytics_engine):
        super().__init__()

        self.analytics = analytics_engine

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Build the analytics interface."""

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(18)

        title = QLabel("Analytics")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Analyze water consumption trends and quality conditions"
        )
        subtitle.setObjectName("PageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        filter_card = QFrame()
        filter_card.setObjectName("Card")

        filter_layout = QHBoxLayout(filter_card)

        location_label = QLabel("Select Location:")

        self.location_combo = QComboBox()
        self.location_combo.setMinimumWidth(280)

        self.location_combo.currentIndexChanged.connect(
            self.refresh_selected_location
        )

        filter_layout.addWidget(location_label)
        filter_layout.addWidget(self.location_combo)
        filter_layout.addStretch()

        main_layout.addWidget(filter_card)

        chart_card = QFrame()
        chart_card.setObjectName("Card")

        chart_layout = QVBoxLayout(chart_card)

        chart_title = QLabel(
            "Consumption Trend"
        )
        chart_title.setObjectName("CardTitle")

        chart_layout.addWidget(chart_title)

        if FigureCanvasQTAgg is not None:

            self.figure = Figure(
                figsize=(7, 3.5)
            )

            self.canvas = FigureCanvasQTAgg(
                self.figure
            )

            chart_layout.addWidget(
                self.canvas
            )

        else:

            self.figure = None
            self.canvas = None

            error_label = QLabel(
                "Matplotlib is not installed. "
                "Install the required packages to view charts."
            )

            error_label.setWordWrap(True)

            chart_layout.addWidget(
                error_label
            )

        main_layout.addWidget(
            chart_card,
            1,
        )

        summary_card = QFrame()
        summary_card.setObjectName("Card")

        summary_layout = QVBoxLayout(
            summary_card
        )

        summary_title = QLabel(
            "Location Performance"
        )

        summary_title.setObjectName(
            "CardTitle"
        )

        summary_layout.addWidget(
            summary_title
        )

        self.summary_table = QTableWidget()

        self.summary_table.setColumnCount(
            6
        )

        self.summary_table.setHorizontalHeaderLabels(
            [
                "Location",
                "Readings",
                "Avg. Usage",
                "Quality",
                "Trend",
                "Alerts",
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
            summary_card
        )

    def refresh(self):
        """Refresh all analytics information."""

        self.refresh_locations()
        self.refresh_summary_table()
        self.refresh_chart()

    def refresh_locations(self):
        """Load locations into the filter."""

        current_id = (
            self.location_combo.currentData()
        )

        self.location_combo.blockSignals(
            True
        )

        self.location_combo.clear()

        self.location_combo.addItem(
            "All Locations",
            None,
        )

        locations = self.analytics.get_locations()

        for location in locations:

            self.location_combo.addItem(
                location.name,
                location.location_id,
            )

        self.location_combo.blockSignals(
            False
        )

        if current_id is not None:

            index = self.location_combo.findData(
                current_id
            )

            if index >= 0:
                self.location_combo.setCurrentIndex(
                    index
                )

    def refresh_selected_location(self):
        """Refresh chart when location changes."""

        self.refresh_chart()

    def refresh_chart(self):
        """Draw the consumption trend chart."""

        if self.figure is None:
            return

        self.figure.clear()

        axis = self.figure.add_subplot(
            111
        )

        location_id = (
            self.location_combo.currentData()
        )

        data = self.analytics.consumption_trend(
            location_id
        )

        if not data:

            axis.text(
                0.5,
                0.5,
                "No reading data available",
                horizontalalignment="center",
                verticalalignment="center",
                transform=axis.transAxes,
            )

            axis.set_axis_off()

            self.canvas.draw()

            return

        dates = [
            item["date"]
            for item in data
        ]

        consumption = [
            item["consumption"]
            for item in data
        ]

        axis.plot(
            dates,
            consumption,
            marker="o",
            linewidth=2,
        )

        axis.set_title(
            "Daily Water Consumption"
        )

        axis.set_xlabel(
            "Date"
        )

        axis.set_ylabel(
            "Consumption (Liters)"
        )

        axis.grid(
            True,
            alpha=0.25,
        )

        self.figure.autofmt_xdate()

        self.figure.tight_layout()

        self.canvas.draw()

    def refresh_summary_table(self):
        """Refresh location performance table."""

        summaries = (
            self.analytics.location_performance()
        )

        self.summary_table.setRowCount(
            len(summaries)
        )

        for row, summary in enumerate(
            summaries
        ):

            values = [
                summary["location"],
                summary["readings"],
                f'{summary["average_consumption"]:.1f} L',
                summary["quality_status"],
                summary["trend"],
                summary["alerts"],
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

                self.summary_table.setItem(
                    row,
                    column,
                    item
                )
