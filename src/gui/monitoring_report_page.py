"""
AquaGuard - Monitoring Report Page

Generates a location-wise monitoring report containing:
- Water consumption
- Water quality status
- Alerts
- Trends
- Conservation recommendations
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)


class MonitoringReportPage(QWidget):
    """Page for generating and viewing monitoring reports."""

    def __init__(self, analytics_engine):
        super().__init__()

        self.analytics = analytics_engine

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Build the monitoring report interface."""

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        main_layout.setSpacing(18)

        title = QLabel(
            "Monitoring Report"
        )

        title.setObjectName(
            "PageTitle"
        )

        subtitle = QLabel(
            "Generate a complete water-monitoring summary"
        )

        subtitle.setObjectName(
            "PageSubtitle"
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        control_card = QFrame()

        control_card.setObjectName(
            "Card"
        )

        control_layout = QHBoxLayout(
            control_card
        )

        location_label = QLabel(
            "Report Location:"
        )

        self.location_combo = QComboBox()

        self.location_combo.setMinimumWidth(
            300
        )

        self.location_combo.currentIndexChanged.connect(
            self.generate_report
        )

        generate_button = QPushButton(
            "📄 Generate Report"
        )

        generate_button.setObjectName(
            "PrimaryButton"
        )

        generate_button.clicked.connect(
            self.generate_report
        )

        control_layout.addWidget(
            location_label
        )

        control_layout.addWidget(
            self.location_combo
        )

        control_layout.addWidget(
            generate_button
        )

        control_layout.addStretch()

        main_layout.addWidget(
            control_card
        )

        report_card = QFrame()

        report_card.setObjectName(
            "Card"
        )

        report_layout = QVBoxLayout(
            report_card
        )

        report_title = QLabel(
            "Water Monitoring Report"
        )

        report_title.setObjectName(
            "CardTitle"
        )

        report_layout.addWidget(
            report_title
        )

        self.report_browser = QTextBrowser()

        self.report_browser.setOpenExternalLinks(
            False
        )

        report_layout.addWidget(
            self.report_browser
        )

        main_layout.addWidget(
            report_card,
            1,
        )

    def refresh(self):
        """Refresh locations and generate the report."""

        self.refresh_locations()
        self.generate_report()

    def refresh_locations(self):
        """Load locations into the report selector."""

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

    def generate_report(self):
        """Generate the selected monitoring report."""

        location_id = (
            self.location_combo.currentData()
        )

        if location_id is None:

            self.generate_overall_report()

            return

        report = (
            self.analytics.get_monitoring_report(
                location_id
            )
        )

        if report is None:

            self.report_browser.setHtml(
                """
                <h2>No Data Available</h2>
                <p>
                There are no water readings available
                for the selected location.
                </p>
                """
            )

            return

        self.report_browser.setHtml(
            self.build_report_html(
                report
            )
        )

    def generate_overall_report(self):
        """Generate a report covering all locations."""

        reports = (
            self.analytics.get_all_monitoring_reports()
        )

        if not reports:

            self.report_browser.setHtml(
                """
                <h2>No Monitoring Data</h2>
                <p>
                Add water readings to generate a
                monitoring report.
                </p>
                """
            )

            return

        html_parts = [
            """
            <html>
            <body>
            <h1>AquaGuard Water Monitoring Report</h1>
            <hr>
            """
        ]

        for report in reports:

            html_parts.append(
                self.build_report_section(
                    report
                )
            )

        html_parts.append(
            """
            </body>
            </html>
            """
        )

        self.report_browser.setHtml(
            "".join(html_parts)
        )

    def build_report_html(self, report):
        """Build HTML for a single monitoring report."""

        return f"""
        <html>
        <body>
        {self.build_report_section(report)}
        </body>
        </html>
        """

    def build_report_section(self, report):
        """Build one report section."""

        location_name = getattr(
            report,
            "location_name",
            "Unknown Location",
        )

        location_type = getattr(
            report,
            "location_type",
            "Monitoring Location",
        )

        total_consumption = getattr(
            report,
            "total_consumption",
            0,
        )

        average_consumption = getattr(
            report,
            "average_consumption",
            0,
        )

        quality_status = getattr(
            report,
            "quality_status",
            "Unknown",
        )

        trend = getattr(
            report,
            "trend",
            "No trend available",
        )

        readings_count = getattr(
            report,
            "readings_count",
            0,
        )

        alerts = getattr(
            report,
            "alerts",
            [],
        )

        recommendations = getattr(
            report,
            "recommendations",
            [],
        )

        alert_html = ""

        if alerts:

            alert_html = "".join(
                f"<li>{alert}</li>"
                for alert in alerts
            )

        else:

            alert_html = (
                "<li>No active alerts.</li>"
            )

        recommendation_html = ""

        if recommendations:

            recommendation_html = "".join(
                f"<li>{recommendation}</li>"
                for recommendation in recommendations
            )

        else:

            recommendation_html = (
                "<li>Continue monitoring and conserving water.</li>"
            )

        return f"""
        <div>
            <h2>{location_name}</h2>

            <p>
                <b>Location Type:</b>
                {location_type}
            </p>

            <h3>Consumption Summary</h3>

            <ul>
                <li>
                    Readings Recorded:
                    {readings_count}
                </li>

                <li>
                    Total Consumption:
                    {total_consumption:.1f} L
                </li>

                <li>
                    Average Daily Consumption:
                    {average_consumption:.1f} L
                </li>

                <li>
                    Consumption Trend:
                    {trend}
                </li>
            </ul>

            <h3>Water Quality Status</h3>

            <p>
                <b>{quality_status}</b>
            </p>

            <h3>Alerts</h3>

            <ul>
                {alert_html}
            </ul>

            <h3>Recommended Conservation Actions</h3>

            <ul>
                {recommendation_html}
            </ul>

            <hr>
        </div>
        """

    def refresh_report(self):
        """Compatibility method for the main window."""

        self.refresh()
