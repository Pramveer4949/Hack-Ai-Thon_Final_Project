"""
AquaGuard - Water Reading Model

Defines the WaterReading class used to store and evaluate
water consumption and basic water-quality observations.
"""

from dataclasses import dataclass
from datetime import date


@dataclass
class WaterReading:
    """
    Represents one water monitoring reading.

    Attributes:
        reading_id: Unique identifier for the reading.
        location_id: ID of the monitored location.
        reading_date: Date of the reading.
        consumption_liters: Daily water consumption in liters.
        ph: Measured pH value.
        turbidity_ntu: Measured turbidity in NTU.
        notes: Optional observation notes.
    """

    reading_id: int
    location_id: int
    reading_date: date
    consumption_liters: float
    ph: float
    turbidity_ntu: float
    notes: str = ""

    # AquaGuard demonstration thresholds.
    # These values can be changed later from the application.
    PH_MIN = 6.5
    PH_MAX = 8.5
    TURBIDITY_MAX = 5.0
    DAILY_CONSUMPTION_ALERT = 1000.0

    @property
    def quality_status(self) -> str:
        """Return the water-quality status."""

        if self.ph < self.PH_MIN or self.ph > self.PH_MAX:
            return "Unsafe"

        if self.turbidity_ntu > self.TURBIDITY_MAX:
            return "Unsafe"

        return "Safe"

    @property
    def consumption_status(self) -> str:
        """Return the daily consumption status."""

        if self.consumption_liters > self.DAILY_CONSUMPTION_ALERT:
            return "Excessive"

        return "Normal"

    @property
    def has_quality_alert(self) -> bool:
        """Return True when a water-quality problem is detected."""

        return self.quality_status == "Unsafe"

    @property
    def has_consumption_alert(self) -> bool:
        """Return True when excessive consumption is detected."""

        return self.consumption_status == "Excessive"

    def alert_messages(self) -> list[str]:
        """Generate alert messages for this reading."""

        alerts = []

        if self.ph < self.PH_MIN:
            alerts.append(
                f"pH is too low ({self.ph:.2f}). "
                "Inspect the water source and retest."
            )

        elif self.ph > self.PH_MAX:
            alerts.append(
                f"pH is too high ({self.ph:.2f}). "
                "Inspect the water source and retest."
            )

        if self.turbidity_ntu > self.TURBIDITY_MAX:
            alerts.append(
                f"Turbidity is high ({self.turbidity_ntu:.2f} NTU). "
                "Check filtration and retest the sample."
            )

        if self.consumption_liters > self.DAILY_CONSUMPTION_ALERT:
            alerts.append(
                f"Daily consumption is excessive "
                f"({self.consumption_liters:.0f} L). "
                "Check for leaks and reduce unnecessary usage."
            )

        return alerts

    def overall_status(self) -> str:
        """Return the overall status of the reading."""

        if self.has_quality_alert:
            return "Unsafe"

        if self.has_consumption_alert:
            return "Warning"

        return "Safe"
