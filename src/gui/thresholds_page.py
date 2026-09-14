"""
AquaGuard - Thresholds Page

Displays the configured thresholds used by AquaGuard
to identify abnormal water readings.
"""

from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class ThresholdsPage(QWidget):
    """Page displaying AquaGuard monitoring thresholds."""

    def __init__(self, analytics_engine):
        super().__init__()

        self.analytics = analytics_engine

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        """Build the thresholds interface."""

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            25,
            25,
            25,
            25,
        )

        main_layout.setSpacing(18)

        title = QLabel(
            "Monitoring Thresholds"
        )

        title.setObjectName(
            "PageTitle"
        )

        subtitle = QLabel(
            "Reference values used to identify abnormal conditions"
        )

        subtitle.setObjectName(
            "PageSubtitle"
        )

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            subtitle
        )

        grid_card = QFrame()

        grid_card.setObjectName(
            "Card"
        )

        grid_layout = QGridLayout(
            grid_card
        )

        grid_layout.setContentsMargins(
            30,
            30,
            30,
            30,
        )

        grid_layout.setHorizontalSpacing(
            25
        )

        grid_layout.setVerticalSpacing(
            20
        )

        ph_title = QLabel(
            "pH Range"
        )

        ph_title.setObjectName(
            "CardTitle"
        )

        self.ph_value = QLabel(
            "--"
        )

        self.ph_value.setObjectName(
            "ThresholdValue"
        )

        ph_description = QLabel(
            "Readings outside this range are flagged "
            "as potential water-quality concerns."
        )

        ph_description.setWordWrap(
            True
        )

        turbidity_title = QLabel(
            "Maximum Turbidity"
        )

        turbidity_title.setObjectName(
            "CardTitle"
        )

        self.turbidity_value = QLabel(
            "--"
        )

        self.turbidity_value.setObjectName(
            "ThresholdValue"
        )

        turbidity_description = QLabel(
            "Higher turbidity readings are flagged "
            "for further attention."
        )

        turbidity_description.setWordWrap(
            True
        )

        consumption_title = QLabel(
            "Daily Consumption Alert"
        )

        consumption_title.setObjectName(
            "CardTitle"
        )

        self.consumption_value = QLabel(
            "--"
        )

        self.consumption_value.setObjectName(
            "ThresholdValue"
        )

        consumption_description = QLabel(
            "Consumption above this configured value "
            "generates an excessive-use alert."
        )

        consumption_description.setWordWrap(
            True
        )

        grid_layout.addWidget(
            ph_title,
            0,
            0,
        )

        grid_layout.addWidget(
            self.ph_value,
            1,
            0,
        )

        grid_layout.addWidget(
            ph_description,
            2,
            0,
        )

        grid_layout.addWidget(
            turbidity_title,
            0,
            1,
        )

        grid_layout.addWidget(
            self.turbidity_value,
            1,
            1,
        )

        grid_layout.addWidget(
            turbidity_description,
            2,
            1,
        )

        grid_layout.addWidget(
            consumption_title,
            0,
            2,
        )

        grid_layout.addWidget(
            self.consumption_value,
            1,
            2,
        )

        grid_layout.addWidget(
            consumption_description,
            2,
            2,
        )

        main_layout.addWidget(
            grid_card
        )

        note_card = QFrame()

        note_card.setObjectName(
            "Card"
        )

        note_layout = QVBoxLayout(
            note_card
        )

        note_title = QLabel(
            "Important Note"
        )

        note_title.setObjectName(
            "CardTitle"
        )

        note_text = QLabel(
            "These thresholds are configurable demonstration "
            "values for the AquaGuard prototype. They are "
            "intended for monitoring and educational purposes "
            "and should not be treated as a substitute for "
            "official laboratory testing or local regulatory standards."
        )

        note_text.setWordWrap(
            True
        )

        note_layout.addWidget(
            note_title
        )

        note_layout.addWidget(
            note_text
        )

        main_layout.addWidget(
            note_card
        )

        main_layout.addStretch()

    def refresh(self):
        """Refresh threshold values from the analytics engine."""

        thresholds = (
            self.analytics.get_thresholds()
        )

        self.ph_value.setText(
            f'{thresholds["ph_min"]:.1f} – '
            f'{thresholds["ph_max"]:.1f}'
        )

        self.turbidity_value.setText(
            f'{thresholds["turbidity_max"]:.1f} NTU'
        )

        self.consumption_value.setText(
            f'{thresholds["consumption_alert"]:.0f} L/day'
        )

    def refresh_thresholds(self):
        """Compatibility method for the main window."""

        self.refresh()
