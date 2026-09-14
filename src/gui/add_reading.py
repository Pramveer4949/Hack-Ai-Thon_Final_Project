"""
AquaGuard - Add Reading Page

Interface for entering and assessing water consumption
and basic water-quality observations.
"""

from datetime import date

from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)

from models.water_reading import WaterReading


class AddReadingPage(QWidget):
    """Page used to add a new water monitoring reading."""

    def __init__(self, database):
        super().__init__()

        self.database = database

        self.setup_ui()
        self.refresh_locations()

    def setup_ui(self):
        """Build the add-reading interface."""

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        main_layout.setSpacing(18)

        title = QLabel("Add Water Reading")
        title.setObjectName("PageTitle")

        subtitle = QLabel(
            "Record daily consumption and basic water-quality observations"
        )

        subtitle.setObjectName("PageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        form_card = QFrame()
        form_card.setObjectName("Card")

        form_layout = QFormLayout(form_card)

        form_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        form_layout.setSpacing(17)

        self.location_combo = QComboBox()

        self.date_input = QLineEdit()
        self.date_input.setText(
            date.today().isoformat()
        )

        self.consumption_input = QDoubleSpinBox()

        self.consumption_input.setRange(
            0,
            100000,
        )

        self.consumption_input.setDecimals(2)
        self.consumption_input.setSuffix(" L")

        self.ph_input = QDoubleSpinBox()

        self.ph_input.setRange(
            0,
            14,
        )

        self.ph_input.setDecimals(2)
        self.ph_input.setSingleStep(0.1)
        self.ph_input.setValue(7.0)

        self.turbidity_input = QDoubleSpinBox()

        self.turbidity_input.setRange(
            0,
            100000,
        )

        self.turbidity_input.setDecimals(2)
        self.turbidity_input.setSuffix(" NTU")

        self.notes_input = QTextEdit()

        self.notes_input.setPlaceholderText(
            "Optional notes about the water sample..."
        )

        self.notes_input.setMaximumHeight(
            120
        )

        form_layout.addRow(
            "Monitoring Location:",
            self.location_combo,
        )

        form_layout.addRow(
            "Reading Date:",
            self.date_input,
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

        main_layout.addWidget(
            form_card
        )

        button_layout = QHBoxLayout()

        self.assess_button = QPushButton(
            "🔍 Assess Reading"
        )

        self.assess_button.clicked.connect(
            self.assess_reading
        )

        self.save_button = QPushButton(
            "💾 Save Reading"
        )

        self.save_button.setObjectName(
            "PrimaryButton"
        )

        self.save_button.clicked.connect(
            self.save_reading
        )

        clear_button = QPushButton(
            "↺ Clear"
        )

        clear_button.clicked.connect(
            self.clear_form
        )

        button_layout.addWidget(
            self.assess_button
        )

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            clear_button
        )

        button_layout.addStretch()

        main_layout.addLayout(
            button_layout
        )

        assessment_card = QFrame()
        assessment_card.setObjectName(
            "Card"
        )

        assessment_layout = QVBoxLayout(
            assessment_card
        )

        assessment_title = QLabel(
            "Live Assessment"
        )

        assessment_title.setObjectName(
            "CardTitle"
        )

        self.assessment_label = QLabel(
            "Enter the reading values and click "
            "\"Assess Reading\"."
        )

        self.assessment_label.setWordWrap(
            True
        )

        self.assessment_label.setObjectName(
            "Assessment"
        )

        assessment_layout.addWidget(
            assessment_title
        )

        assessment_layout.addWidget(
            self.assessment_label
        )

        main_layout.addWidget(
            assessment_card
        )

        main_layout.addStretch()

    def refresh_locations(self):
        """Load available monitoring locations."""

        current_id = self.location_combo.currentData()

        self.location_combo.blockSignals(
            True
        )

        self.location_combo.clear()

        locations = self.database.get_locations()

        for location in locations:

            display_text = (
                f"{location.name} "
                f"({location.location_type})"
            )

            self.location_combo.addItem(
                display_text,
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

    def get_current_values(self):
        """Return the values currently entered by the user."""

        return {
            "location_id": self.location_combo.currentData(),
            "date": self.date_input.text().strip(),
            "consumption": self.consumption_input.value(),
            "ph": self.ph_input.value(),
            "turbidity": self.turbidity_input.value(),
            "notes": self.notes_input.toPlainText().strip(),
        }

    def validate_date(self, date_text):
        """Validate the entered date."""

        try:
            return date.fromisoformat(
                date_text
            )

        except ValueError:
            return None

    def assess_reading(self):
        """Assess the entered reading."""

        values = self.get_current_values()

        if values["location_id"] is None:

            self.assessment_label.setText(
                "🔴 Please select a monitoring location."
            )

            return

        reading_date = self.validate_date(
            values["date"]
        )

        if reading_date is None:

            self.assessment_label.setText(
                "🔴 Invalid date. Use YYYY-MM-DD."
            )

            return

        reading = WaterReading(
            reading_id=0,
            location_id=values["location_id"],
            reading_date=reading_date,
            consumption_liters=values["consumption"],
            ph=values["ph"],
            turbidity_ntu=values["turbidity"],
            notes=values["notes"],
        )

        messages = reading.alert_messages()

        if not messages:

            self.assessment_label.setText(
                "🟢 SAFE\n\n"
                "The reading is within all configured "
                "quality and consumption thresholds."
            )

            return

        quality_alert = (
            reading.has_quality_alert
        )

        consumption_alert = (
            reading.has_consumption_alert
        )

        if quality_alert:

            status = (
                "🔴 UNSAFE / QUALITY ALERT"
            )

        elif consumption_alert:

            status = (
                "🟡 HIGH CONSUMPTION"
            )

        else:

            status = (
                "🟡 WARNING"
            )

        message_text = "\n".join(
            f"• {message}"
            for message in messages
        )

        self.assessment_label.setText(
            f"{status}\n\n{message_text}"
        )

    def save_reading(self):
        """Validate and save the current reading."""

        values = self.get_current_values()

        if values["location_id"] is None:

            QMessageBox.warning(
                self,
                "Location Required",
                "Please select a monitoring location.",
            )

            return

        reading_date = self.validate_date(
            values["date"]
        )

        if reading_date is None:

            QMessageBox.warning(
                self,
                "Invalid Date",
                "Please enter the date in YYYY-MM-DD format.",
            )

            return

        reading = WaterReading(
            reading_id=0,
            location_id=values["location_id"],
            reading_date=reading_date,
            consumption_liters=values["consumption"],
            ph=values["ph"],
            turbidity_ntu=values["turbidity"],
            notes=values["notes"],
        )

        try:

            self.database.add_reading(
                reading
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Save Error",
                f"Could not save the reading.\n\n{error}",
            )

            return

        QMessageBox.information(
            self,
            "Reading Saved",
            "Water reading has been saved successfully.",
        )

        self.clear_form()

        self.reading_saved()

    def reading_saved(self):
        """Hook for the main window after saving."""

        parent = self.parent()

        if parent is not None:

            refresh_method = getattr(
                parent,
                "refresh_all",
                None,
            )

            if callable(refresh_method):
                refresh_method()

    def clear_form(self):
        """Clear all reading fields."""

        self.date_input.setText(
            date.today().isoformat()
        )

        self.consumption_input.setValue(
            0
        )

        self.ph_input.setValue(
            7.0
        )

        self.turbidity_input.setValue(
            0
        )

        self.notes_input.clear()

        self.assessment_label.setText(
            'Enter the reading values and click '
            '"Assess Reading".'
        )

    def refresh(self):
        """Refresh the page data."""

        self.refresh_locations()
