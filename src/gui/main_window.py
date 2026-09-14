"""
AquaGuard - Main Window

Main graphical user interface for the AquaGuard
Community Water Quality & Usage Monitor.
"""

from datetime import date

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QDoubleSpinBox,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from database.database_manager import DatabaseManager
from analytics.analytics_engine import AnalyticsEngine
from models.location import LocationUser
from models.water_reading import WaterReading


class AquaGuardWindow(QMainWindow):
    """Main AquaGuard application window."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("AquaGuard - Water Quality & Usage Monitor")
        self.setMinimumSize(1200, 750)

        self.database = DatabaseManager()

        self.pages = QStackedWidget()

        self.dashboard_page = self.create_dashboard_page()
        self.reading_page = self.create_reading_page()
        self.analytics_page = self.create_analytics_page()
        self.alerts_page = self.create_alerts_page()
        self.locations_page = self.create_locations_page()
        self.report_page = self.create_report_page()
        self.thresholds_page = self.create_thresholds_page()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.reading_page)
        self.pages.addWidget(self.analytics_page)
        self.pages.addWidget(self.alerts_page)
        self.pages.addWidget(self.locations_page)
        self.pages.addWidget(self.report_page)
        self.pages.addWidget(self.thresholds_page)

        self.create_main_layout()
        self.refresh_all()

    # ------------------------------------------------------------------
    # Main Layout
    # ------------------------------------------------------------------

    def create_main_layout(self):
        """Create the main application layout."""

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        sidebar = self.create_sidebar()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages, 1)

        self.setCentralWidget(central_widget)

    def create_sidebar(self):
        """Create the navigation sidebar."""

        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(245)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 25, 18, 20)
        layout.setSpacing(10)

        logo = QLabel("💧 AquaGuard")
        logo.setObjectName("Logo")

        subtitle = QLabel("Water Intelligence System")
        subtitle.setObjectName("SidebarSubtitle")

        layout.addWidget(logo)
        layout.addWidget(subtitle)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("SidebarSeparator")
        layout.addWidget(separator)

        buttons = [
            ("◉  Dashboard", 0),
            ("＋  Add Reading", 1),
            ("◈  Analytics", 2),
            ("⚠  Alerts", 3),
            ("▣  Locations", 4),
            ("▤  Monitoring Report", 5),
            ("⚙  Thresholds", 6),
        ]

        for text, index in buttons:
            button = QPushButton(text)
            button.setObjectName("NavButton")
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked=False, i=index: self.pages.setCurrentIndex(i)
            )
            layout.addWidget(button)

        layout.addStretch()

        demo_button = QPushButton("🌱 Load Demo Data")
        demo_button.setObjectName("DemoButton")
        demo_button.clicked.connect(self.load_demo_data)

        layout.addWidget(demo_button)

        status = QLabel("● System Ready")
        status.setObjectName("SystemStatus")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(status)

        return sidebar

    # ------------------------------------------------------------------
    # Dashboard
    # ------------------------------------------------------------------

    def create_dashboard_page(self):
        """Create the dashboard page."""

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)

        title = QLabel("Dashboard")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Community water quality, consumption and conservation overview"
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.kpi_grid = QGridLayout()
        self.kpi_grid.setSpacing(15)

        self.locations_card = self.create_kpi_card(
            "📍",
            "Locations",
            "0",
        )

        self.readings_card = self.create_kpi_card(
            "💧",
            "Readings",
            "0",
        )

        self.consumption_card = self.create_kpi_card(
            "📊",
            "Average Usage",
            "0 L",
        )

        self.alerts_card = self.create_kpi_card(
            "⚠",
            "Active Alerts",
            "0",
        )

        self.kpi_grid.addWidget(self.locations_card, 0, 0)
        self.kpi_grid.addWidget(self.readings_card, 0, 1)
        self.kpi_grid.addWidget(self.consumption_card, 0, 2)
        self.kpi_grid.addWidget(self.alerts_card, 0, 3)

        layout.addLayout(self.kpi_grid)

        content_grid = QGridLayout()
        content_grid.setSpacing(20)

        quality_frame = QFrame()
        quality_frame.setObjectName("Card")

        quality_layout = QVBoxLayout(quality_frame)

        quality_title = QLabel("Water Quality Overview")
        quality_title.setObjectName("CardTitle")

        self.quality_status_label = QLabel("No Data")
        self.quality_status_label.setObjectName("LargeStatus")

        self.quality_score_label = QLabel("Quality Score: 0%")
        self.quality_score_label.setObjectName("CardText")

        self.conservation_score_label = QLabel(
            "Conservation Score: 0%"
        )
        self.conservation_score_label.setObjectName("CardText")

        quality_layout.addWidget(quality_title)
        quality_layout.addSpacing(15)
        quality_layout.addWidget(self.quality_status_label)
        quality_layout.addWidget(self.quality_score_label)
        quality_layout.addWidget(self.conservation_score_label)
        quality_layout.addStretch()

        content_grid.addWidget(quality_frame, 0, 0)

        summary_frame = QFrame()
        summary_frame.setObjectName("Card")

        summary_layout = QVBoxLayout(summary_frame)

        summary_title = QLabel("Location Summary")
        summary_title.setObjectName("CardTitle")

        self.dashboard_table = QTableWidget()
        self.dashboard_table.setColumnCount(4)
        self.dashboard_table.setHorizontalHeaderLabels(
            [
                "Location",
                "Average Usage",
                "Quality",
                "Trend",
            ]
        )

        self.dashboard_table.horizontalHeader().setStretchLastSection(True)
        self.dashboard_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        summary_layout.addWidget(summary_title)
        summary_layout.addWidget(self.dashboard_table)

        content_grid.addWidget(summary_frame, 0, 1)

        layout.addLayout(content_grid, 1)

        return page

    def create_kpi_card(self, icon, title, value):
        """Create a dashboard KPI card."""

        card = QFrame()
        card.setObjectName("KPICard")

        layout = QVBoxLayout(card)

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

    # ------------------------------------------------------------------
    # Add Reading
    # ------------------------------------------------------------------

    def create_reading_page(self):
        """Create the add-reading page."""

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("Add Water Reading")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Record daily water consumption and basic quality observations"
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        form_card = QFrame()
        form_card.setObjectName("Card")

        form_layout = QFormLayout(form_card)
        form_layout.setContentsMargins(25, 25, 25, 25)
        form_layout.setSpacing(18)

        self.reading_location = QComboBox()

        self.reading_date = QLineEdit()
        self.reading_date.setText(date.today().isoformat())

        self.consumption_input = QDoubleSpinBox()
        self.consumption_input.setRange(0, 100000)
        self.consumption_input.setDecimals(2)
        self.consumption_input.setSuffix(" L")

        self.ph_input = QDoubleSpinBox()
        self.ph_input.setRange(0, 14)
        self.ph_input.setDecimals(2)
        self.ph_input.setValue(7.0)

        self.turbidity_input = QDoubleSpinBox()
        self.turbidity_input.setRange(0, 100000)
        self.turbidity_input.setDecimals(2)
        self.turbidity_input.setSuffix(" NTU")

        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)

        form_layout.addRow(
            "Location:",
            self.reading_location,
        )

        form_layout.addRow(
            "Date:",
            self.reading_date,
        )

        form_layout.addRow(
            "Daily Consumption:",
            self.consumption_input,
        )

        form_layout.addRow(
            "pH:",
            self.ph_input,
        )

        form_layout.addRow(
            "Turbidity:",
            self.turbidity_input,
        )

        form_layout.addRow(
            "Notes:",
            self.notes_input,
        )

        layout.addWidget(form_card)

        button_layout = QHBoxLayout()

        assess_button = QPushButton("🔍 Assess Reading")
        assess_button.clicked.connect(self.assess_reading)

        save_button = QPushButton("💾 Save Reading")
        save_button.setObjectName("PrimaryButton")
        save_button.clicked.connect(self.save_reading)

        button_layout.addWidget(assess_button)
        button_layout.addWidget(save_button)
        button_layout.addStretch()

        layout.addLayout(button_layout)

        self.assessment_label = QLabel(
            "Enter values and assess the reading."
        )
        self.assessment_label.setObjectName("Assessment")

        layout.addWidget(self.assessment_label)
        layout.addStretch()

        return page

    def assess_reading(self):
        """Assess the current water reading."""

        consumption = self.consumption_input.value()
        ph = self.ph_input.value()
        turbidity = self.turbidity_input.value()

        quality_safe = (
            WaterReading.PH_MIN <= ph <= WaterReading.PH_MAX
            and turbidity <= WaterReading.TURBIDITY_MAX
        )

        consumption_safe = (
            consumption <= WaterReading.DAILY_CONSUMPTION_ALERT
        )

        if quality_safe and consumption_safe:
            self.assessment_label.setText(
                "🟢 SAFE — Water quality and consumption are within "
                "configured thresholds."
            )
        elif not quality_safe:
            self.assessment_label.setText(
                "🔴 UNSAFE — One or more water-quality values require "
                "attention."
            )
        else:
            self.assessment_label.setText(
                "🟡 WARNING — Water quality is acceptable, but "
                "consumption is excessive."
            )

    def save_reading(self):
        """Save the entered water reading."""

        if self.reading_location.currentData() is None:
            QMessageBox.warning(
                self,
                "No Location",
                "Please create a location before adding a reading.",
            )
            return

        try:
            reading_date = date.fromisoformat(
                self.reading_date.text().strip()
            )
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Date",
                "Please enter the date in YYYY-MM-DD format.",
            )
            return

        reading = WaterReading(
            reading_id=0,
            location_id=self.reading_location.currentData(),
            reading_date=reading_date,
            consumption_liters=self.consumption_input.value(),
            ph=self.ph_input.value(),
            turbidity_ntu=self.turbidity_input.value(),
            notes=self.notes_input.toPlainText().strip(),
        )

        self.database.add_reading(reading)

        QMessageBox.information(
            self,
            "Reading Saved",
            "Water reading saved successfully.",
        )

        self.notes_input.clear()
        self.refresh_all()

    # ------------------------------------------------------------------
    # Analytics
    # ------------------------------------------------------------------

    def create_analytics_page(self):
        """Create analytics page."""

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("Analytics")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Analyse consumption patterns and water-quality performance"
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.analytics_location = QComboBox()
        self.analytics_location.currentIndexChanged.connect(
            self.refresh_analytics
        )

        layout.addWidget(QLabel("Location:"))
        layout.addWidget(self.analytics_location)

        self.analytics_table = QTableWidget()
        self.analytics_table.setColumnCount(7)

        self.analytics_table.setHorizontalHeaderLabels(
            [
                "Location",
                "Type",
                "Avg Usage",
                "Quality",
                "Trend",
                "Alerts",
                "Conservation",
            ]
        )

        self.analytics_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.analytics_table.horizontalHeader().setStretchLastSection(
            True
        )

        layout.addWidget(self.analytics_table)

        return page

    def refresh_analytics(self):
        """Refresh analytics information."""

        locations = self.database.get_locations()
        readings = self.database.get_readings()

        selected_id = self.analytics_location.currentData()

        if selected_id is not None:
            readings = [
                reading
                for reading in readings
                if reading.location_id == selected_id
            ]

        engine = AnalyticsEngine(locations, readings)

        summaries = engine.location_summary()

        self.analytics_table.setRowCount(len(summaries))

        for row, summary in enumerate(summaries):

            values = [
                summary["location"],
                summary["type"],
                f'{summary["average_consumption"]:.1f} L',
                summary["quality_status"],
                summary["trend"],
                str(summary["alerts"]),
                summary["conservation_status"],
            ]

            for column, value in enumerate(values):
                self.analytics_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value)),
                )

    # ------------------------------------------------------------------
    # Alerts
    # ------------------------------------------------------------------

    def create_alerts_page(self):
        """Create alerts page."""

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("Alert Center")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Potentially unsafe water conditions and excessive usage"
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.alerts_table = QTableWidget()
        self.alerts_table.setColumnCount(4)

        self.alerts_table.setHorizontalHeaderLabels(
            [
                "Location",
                "Date",
                "Severity",
                "Alert",
            ]
        )

        self.alerts_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.alerts_table.horizontalHeader().setStretchLastSection(
            True
        )

        layout.addWidget(self.alerts_table)

        return page

    def refresh_alerts(self):
        """Refresh alert table."""

        locations = self.database.get_locations()
        readings = self.database.get_readings()

        location_map = {
            location.location_id: location.name
            for location in locations
        }

        alert_rows = []

        for reading in readings:

            messages = reading.alert_messages()

            for message in messages:

                severity = "Critical" if reading.has_quality_alert else "Warning"

                alert_rows.append(
                    (
                        location_map.get(
                            reading.location_id,
                            "Unknown",
                        ),
                        reading.reading_date.isoformat(),
                        severity,
                        message,
                    )
                )

        self.alerts_table.setRowCount(len(alert_rows))

        for row, alert in enumerate(alert_rows):

            for column, value in enumerate(alert):
                self.alerts_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value)),
                )

    # ------------------------------------------------------------------
    # Locations
    # ------------------------------------------------------------------

    def create_locations_page(self):
        """Create locations page."""

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("Locations")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Manage households, schools and community monitoring locations"
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        add_button = QPushButton("＋ New Location")
        add_button.setObjectName("PrimaryButton")
        add_button.clicked.connect(self.add_location)

        layout.addWidget(add_button)

        self.locations_table = QTableWidget()
        self.locations_table.setColumnCount(5)

        self.locations_table.setHorizontalHeaderLabels(
            [
                "Location",
                "Type",
                "Responsible Person",
                "Target / Day",
                "Status",
            ]
        )

        self.locations_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.locations_table.horizontalHeader().setStretchLastSection(
            True
        )

        layout.addWidget(self.locations_table)

        return page

    def add_location(self):
        """Create a new monitoring location."""

        name, accepted = self.simple_input(
            "Location Name",
            "Enter location name:",
        )

        if not accepted or not name.strip():
            return

        location_type, accepted = self.simple_input(
            "Location Type",
            "Enter type (Household, School, Community):",
        )

        if not accepted or not location_type.strip():
            return

        responsible, accepted = self.simple_input(
            "Responsible Person",
            "Enter responsible person:",
        )

        if not accepted or not responsible.strip():
            return

        target, accepted = self.simple_input(
            "Daily Target",
            "Enter target daily consumption in liters:",
        )

        if not accepted:
            return

        try:
            target_value = float(target)
        except ValueError:
            QMessageBox.warning(
                self,
                "Invalid Target",
                "Daily target must be a number.",
            )
            return

        location = LocationUser(
            location_id=0,
            name=name.strip(),
            location_type=location_type.strip(),
            responsible_person=responsible.strip(),
            target_daily_liters=target_value,
        )

        self.database.add_location(location)

        self.refresh_all()

    def simple_input(self, title, label):
        """Display a simple text input dialog."""

        from PySide6.QtWidgets import QInputDialog

        return QInputDialog.getText(
            self,
            title,
            label,
        )

    # ------------------------------------------------------------------
    # Monitoring Report
    # ------------------------------------------------------------------

    def create_report_page(self):
        """Create monitoring report page."""

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("Monitoring Report")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Location-wise consumption, quality, alerts and recommendations"
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.report_location = QComboBox()

        self.report_location.currentIndexChanged.connect(
            self.refresh_report
        )

        layout.addWidget(self.report_location)

        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)

        layout.addWidget(self.report_text)

        return page

    def refresh_report(self):
        """Generate the selected location's monitoring report."""

        location_id = self.report_location.currentData()

        if location_id is None:
            self.report_text.setText(
                "No monitoring location available."
            )
            return

        locations = self.database.get_locations()
        readings = self.database.get_readings()

        engine = AnalyticsEngine(locations, readings)

        report = engine.generate_report(location_id)

        if report is None:
            self.report_text.setText("No report available.")
            return

        lines = [
            "AQUAGUARD MONITORING REPORT",
            "=" * 50,
            "",
            f"Location: {report.location.name}",
            f"Type: {report.location.location_type}",
            f"Responsible Person: "
            f"{report.location.responsible_person}",
            "",
            f"Total Consumption: "
            f"{report.total_consumption:.2f} L",
            f"Average Daily Consumption: "
            f"{report.average_consumption:.2f} L",
            f"Quality Status: {report.quality_status}",
            f"Consumption Trend: {report.trend}",
            f"Conservation Status: "
            f"{report.conservation_status}",
            "",
            "ALERTS",
            "-" * 50,
        ]

        if report.alerts:
            lines.extend(
                f"• {alert}"
                for alert in report.alerts
            )
        else:
            lines.append("No active alerts.")

        lines.extend(
            [
                "",
                "RECOMMENDATIONS",
                "-" * 50,
            ]
        )

        lines.extend(
            f"• {recommendation}"
            for recommendation in report.recommendations
        )

        self.report_text.setText("\n".join(lines))

    # ------------------------------------------------------------------
    # Thresholds
    # ------------------------------------------------------------------

    def create_thresholds_page(self):
        """Create thresholds information page."""

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("Monitoring Thresholds")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Configured demonstration thresholds used for AquaGuard alerts"
        )
        subtitle.setObjectName("PageSubtitle")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        frame = QFrame()
        frame.setObjectName("Card")

        form = QFormLayout(frame)
        form.setContentsMargins(30, 30, 30, 30)
        form.setSpacing(20)

        form.addRow(
            "Minimum pH:",
            QLabel(f"{WaterReading.PH_MIN:.2f}"),
        )

        form.addRow(
            "Maximum pH:",
            QLabel(f"{WaterReading.PH_MAX:.2f}"),
        )

        form.addRow(
            "Maximum Turbidity:",
            QLabel(
                f"{WaterReading.TURBIDITY_MAX:.2f} NTU"
            ),
        )

        form.addRow(
            "Consumption Alert:",
            QLabel(
                f"{WaterReading.DAILY_CONSUMPTION_ALERT:.0f} L/day"
            ),
        )

        layout.addWidget(frame)

        note = QLabel(
            "Note: These are configurable demonstration thresholds "
            "for the prototype and are not a substitute for official "
            "laboratory or regulatory water-quality testing."
        )

        note.setWordWrap(True)
        note.setObjectName("Notice")

        layout.addWidget(note)
        layout.addStretch()

        return page

    # ------------------------------------------------------------------
    # Demo Data
    # ------------------------------------------------------------------

    def load_demo_data(self):
        """Load representative sample data."""

        locations = self.database.get_locations()

        if locations:
            answer = QMessageBox.question(
                self,
                "Load Demo Data",
                "Demo data will be added to the existing database. Continue?",
            )

            if answer != QMessageBox.StandardButton.Yes:
                return

        demo_locations = [
            LocationUser(
                0,
                "Green Valley School",
                "School",
                "School Principal",
                900,
            ),
            LocationUser(
                0,
                "Household 101",
                "Household",
                "Resident",
                700,
            ),
            LocationUser(
                0,
                "Community Center",
                "Community",
                "Community Coordinator",
                1200,
            ),
            LocationUser(
                0,
                "Household 204",
                "Household",
                "Resident",
                750,
            ),
        ]

        created_locations = []

        for location in demo_locations:
            location_id = self.database.add_location(location)

            created_locations.append(
                LocationUser(
                    location_id,
                    location.name,
                    location.location_type,
                    location.responsible_person,
                    location.target_daily_liters,
                )
            )

        sample_values = [
            (650, 7.1, 1.5),
            (720, 7.2, 2.0),
            (810, 7.0, 2.4),
            (950, 6.9, 3.0),
            (1100, 6.8, 4.2),
            (1250, 6.7, 6.5),
            (900, 7.3, 2.2),
        ]

        for location_index, location in enumerate(
            created_locations
        ):

            for day_index, values in enumerate(sample_values):

                consumption, ph, turbidity = values

                consumption += location_index * 60

                if location_index == 3 and day_index >= 4:
                    ph = 5.8
                    turbidity = 8.0

                reading = WaterReading(
                    reading_id=0,
                    location_id=location.location_id,
                    reading_date=date.today().replace(
                        day=max(
                            1,
                            date.today().day - 6 + day_index,
                        )
                    ),
                    consumption_liters=consumption,
                    ph=ph,
                    turbidity_ntu=turbidity,
                    notes="Representative AquaGuard demo reading.",
                )

                self.database.add_reading(reading)

        QMessageBox.information(
            self,
            "Demo Data Loaded",
            "Representative monitoring data has been added successfully.",
        )

        self.refresh_all()

    # ------------------------------------------------------------------
    # Refresh
    # ------------------------------------------------------------------

    def refresh_all(self):
        """Refresh all application data."""

        locations = self.database.get_locations()
        readings = self.database.get_readings()

        engine = AnalyticsEngine(
            locations,
            readings,
        )

        summary = engine.dashboard_summary()

        self.locations_card.value_label.setText(
            str(summary["locations"])
        )

        self.readings_card.value_label.setText(
            str(summary["readings"])
        )

        self.consumption_card.value_label.setText(
            f'{summary["average_consumption"]:.1f} L'
        )

        self.alerts_card.value_label.setText(
            str(summary["active_alerts"])
        )

        self.quality_status_label.setText(
            f'● {summary["overall_quality"]}'
        )

        self.quality_score_label.setText(
            f'Quality Score: {summary["quality_score"]}%'
        )

        self.conservation_score_label.setText(
            f'Conservation Score: '
            f'{summary["conservation_score"]}%'
        )

        self.refresh_dashboard_table(
            engine.location_summary()
        )

        self.refresh_location_table(
            locations,
            readings,
        )

        self.refresh_location_combos(
            locations
        )

        self.refresh_analytics()
        self.refresh_alerts()
        self.refresh_report()

    def refresh_dashboard_table(self, summaries):
        """Refresh dashboard location summary."""

        self.dashboard_table.setRowCount(
            len(summaries)
        )

        for row, summary in enumerate(summaries):

            values = [
                summary["location"],
                f'{summary["average_consumption"]:.1f} L',
                summary["quality_status"],
                summary["trend"],
            ]

            for column, value in enumerate(values):
                self.dashboard_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value)),
                )

    def refresh_location_table(
        self,
        locations,
        readings,
    ):
        """Refresh the locations table."""

        engine = AnalyticsEngine(
            locations,
            readings,
        )

        summaries = {
            item["location_id"]: item
            for item in engine.location_summary()
        }

        self.locations_table.setRowCount(
            len(locations)
        )

        for row, location in enumerate(locations):

            summary = summaries.get(
                location.location_id,
                {},
            )

            values = [
                location.name,
                location.location_type,
                location.responsible_person,
                f"{location.target_daily_liters:.0f} L",
                summary.get(
                    "quality_status",
                    "No Data",
                ),
            ]

            for column, value in enumerate(values):
                self.locations_table.setItem(
                    row,
                    column,
                    QTableWidgetItem(str(value)),
                )

    def refresh_location_combos(self, locations):
        """Refresh location dropdowns."""

        current_reading = self.reading_location.currentData()
        current_analytics = self.analytics_location.currentData()
        current_report = self.report_location.currentData()

        for combo in [
            self.reading_location,
            self.analytics_location,
            self.report_location,
        ]:
            combo.blockSignals(True)
            combo.clear()

        self.analytics_location.addItem(
            "All Locations",
            None,
        )

        for location in locations:

            display = (
                f"{location.name} "
                f"({location.location_type})"
            )

            self.reading_location.addItem(
                display,
                location.location_id,
            )

            self.analytics_location.addItem(
                display,
                location.location_id,
            )

            self.report_location.addItem(
                display,
                location.location_id,
            )

        for combo in [
            self.reading_location,
            self.analytics_location,
            self.report_location,
        ]:
            combo.blockSignals(False)

        self.restore_combo(
            self.reading_location,
            current_reading,
        )

        self.restore_combo(
            self.analytics_location,
            current_analytics,
        )

        self.restore_combo(
            self.report_location,
            current_report,
        )

    def restore_combo(self, combo, value):
        """Restore a combo box selection."""

        if value is None:
            return

        index = combo.findData(value)

        if index >= 0:
            combo.setCurrentIndex(index)


# ----------------------------------------------------------------------
# Application Styling
# ----------------------------------------------------------------------

APP_STYLE = """
QMainWindow {
    background: #f4f8f9;
}

QWidget {
    font-family: "Segoe UI";
    font-size: 14px;
    color: #203238;
}

#Sidebar {
    background: #073b4c;
}

#Logo {
    color: white;
    font-size: 25px;
    font-weight: bold;
}

#SidebarSubtitle {
    color: #a9d6df;
    font-size: 12px;
}

#SidebarSeparator {
    background: #286477;
    max-height: 1px;
}

#NavButton {
    background: transparent;
    color: #d9edf1;
    border: none;
    border-radius: 9px;
    padding: 12px;
    text-align: left;
    font-size: 14px;
}

#NavButton:hover {
    background: #12576a;
}

#DemoButton {
    background: #2a9d8f;
    color: white;
    border: none;
    border-radius: 9px;
    padding: 11px;
    font-weight: bold;
}

#SystemStatus {
    color: #8bd3c7;
    font-size: 12px;
}

#PageTitle {
    font-size: 29px;
    font-weight: bold;
    color: #073b4c;
}

#PageSubtitle {
    color: #64777c;
    font-size: 14px;
}

#Card,
#KPICard {
    background: white;
    border: 1px solid #dce8eb;
    border-radius: 14px;
}

#KPICard {
    padding: 8px;
}

#KPIIcon {
    font-size: 23px;
}

#KPITitle {
    color: #6b7c81;
    font-size: 13px;
}

#KPIValue {
    color: #073b4c;
    font-size: 25px;
    font-weight: bold;
}

#CardTitle {
    color: #073b4c;
    font-size: 17px;
    font-weight: bold;
}

#CardText {
    color: #5d7075;
    padding: 4px;
}

#LargeStatus {
    color: #2a9d8f;
    font-size: 30px;
    font-weight: bold;
}

#PrimaryButton {
    background: #0b7285;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 11px 18px;
    font-weight: bold;
}

#PrimaryButton:hover {
    background: #095c6a;
}

QPushButton {
    background: #e6f1f3;
    color: #164b57;
    border: none;
    border-radius: 8px;
    padding: 10px 16px;
}

QPushButton:hover {
    background: #d4e8eb;
}

QLineEdit,
QComboBox,
QDoubleSpinBox,
QTextEdit {
    background: white;
    border: 1px solid #cbdde1;
    border-radius: 7px;
    padding: 8px;
}

QLineEdit:focus,
QComboBox:focus,
QDoubleSpinBox:focus,
QTextEdit:focus {
    border: 2px solid #2a9d8f;
}

QTableWidget {
    background: white;
    border: 1px solid #dce8eb;
    border-radius: 9px;
    gridline-color: #e6eef0;
    selection-background-color: #d8eff0;
    selection-color: #073b4c;
}

QHeaderView::section {
    background: #edf5f6;
    color: #315b63;
    border: none;
    padding: 9px;
    font-weight: bold;
}

#Assessment {
    background: white;
    border: 1px solid #dce8eb;
    border-radius: 10px;
    padding: 15px;
    font-weight: bold;
}

#Notice {
    background: #fff8e6;
    border: 1px solid #f1d58a;
    border-radius: 9px;
    padding: 12px;
    color: #765b16;
}
"""


def run_application():
    """Start AquaGuard."""

    app = QApplication.instance()

    if app is None:
        app = QApplication([])

    app.setStyleSheet(APP_STYLE)

    window = AquaGuardWindow()
    window.show()

    return app.exec()
