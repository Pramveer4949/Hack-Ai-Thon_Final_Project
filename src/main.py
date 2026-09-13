from datetime import datetime, date
from typing import List


# Project-defined demo thresholds
PH_MIN = 6.5
PH_MAX = 8.5
TURBIDITY_LIMIT = 5.0
CONSUMPTION_LIMIT = 500


class Location:
    def __init__(self, name: str, address: str,
                 location_type: str = "Household"):
        self.name = name
        self.address = address
        self.location_type = location_type

    def __str__(self):
        return f"{self.name} ({self.address})"


class User:
    def __init__(self, user_id: str, name: str,
                 role: str = "Resident"):
        self.user_id = user_id
        self.name = name
        self.role = role

    def __str__(self):
        return f"{self.name} ({self.user_id})"


class WaterReading:
    """Stores one day's complete water data."""

    def __init__(
        self,
        reading_date: date,
        location: Location,
        recorded_by: User,
        consumption: float,
        ph: float,
        turbidity: float
    ):
        self.reading_date = reading_date
        self.location = location
        self.recorded_by = recorded_by
        self.consumption = consumption
        self.ph = ph
        self.turbidity = turbidity

    def is_abnormal(self) -> bool:
        """Checks whether any reading is outside the selected limits."""

        if not (PH_MIN <= self.ph <= PH_MAX):
            return True

        if self.turbidity > TURBIDITY_LIMIT:
            return True

        if self.consumption > CONSUMPTION_LIMIT:
            return True

        return False

    def get_alerts(self) -> List[str]:
        """Returns alerts for abnormal values."""

        alerts = []

        if self.ph < PH_MIN:
            alerts.append(
                f"Low pH ({self.ph}) - acidic water"
            )

        elif self.ph > PH_MAX:
            alerts.append(
                f"High pH ({self.ph}) - alkaline water"
            )

        if self.turbidity > TURBIDITY_LIMIT:
            alerts.append(
                f"High turbidity ({self.turbidity} NTU) "
                f"- water may be unsafe"
            )

        if self.consumption > CONSUMPTION_LIMIT:
            alerts.append(
                f"High consumption ({self.consumption} L) "
                f"- possible wastage"
            )

        return alerts

    def quality_status(self) -> str:
        """Returns the quality status of the water."""

        if self.ph < PH_MIN or self.ph > PH_MAX:
            return "Unsafe"

        if self.turbidity > TURBIDITY_LIMIT:
            return "Unsafe"

        return "Safe"

    def __str__(self):
        return (
            f"{self.reading_date} | "
            f"Consumption: {self.consumption} L | "
            f"pH: {self.ph} | "
            f"Turbidity: {self.turbidity} NTU | "
            f"Quality: {self.quality_status()}"
        )


class MonitoringReport:
    """Generates the complete water monitoring report."""

    def __init__(
        self,
        report_id: str,
        generated_by: User,
        location: Location
    ):
        self.report_id = report_id
        self.generated_by = generated_by
        self.location = location
        self.readings: List[WaterReading] = []
        self.generated_at = datetime.now()

    def add_reading(self, reading: WaterReading):
        """Adds a reading belonging to this location."""

        if reading.location.name == self.location.name:
            self.readings.append(reading)

    def average_consumption(self) -> float:
        if not self.readings:
            return 0.0

        total = sum(
            reading.consumption
            for reading in self.readings
        )

        return total / len(self.readings)

    def consumption_trend(self) -> str:
        """Compares the first and last consumption readings."""

        if len(self.readings) < 2:
            return "Not enough data"

        first = self.readings[0].consumption
        last = self.readings[-1].consumption

        if last > first * 1.15:
            return "Increasing (possible wastage)"

        elif last < first * 0.85:
            return "Decreasing (good conservation)"

        return "Stable"

    def get_all_alerts(self) -> List[str]:
        """Collects alerts from all readings."""

        alerts = []

        for reading in self.readings:
            if reading.is_abnormal():
                alerts.extend(reading.get_alerts())

        return alerts

    def recommendations(self) -> List[str]:
        """Creates simple water conservation recommendations."""

        recommendations = []
        alerts = self.get_all_alerts()

        if self.average_consumption() > 400:
            recommendations.append(
                "Reduce daily water usage and check for leaks."
            )

        if "Increasing" in self.consumption_trend():
            recommendations.append(
                "Consumption is rising - check for leaks or overuse."
            )

        if any(
            "turbidity" in alert.lower()
            for alert in alerts
        ):
            recommendations.append(
                "High turbidity detected - consider filtration "
                "or further water testing."
            )

        if any(
            "pH" in alert
            for alert in alerts
        ):
            recommendations.append(
                "pH is outside the selected safe range - "
                "get the water tested."
            )

        if not recommendations:
            recommendations.append(
                "Water usage and quality are within normal limits. "
                "Keep conserving water."
            )

        return recommendations

    def status(self) -> str:
        if self.get_all_alerts():
            return "ATTENTION NEEDED"

        return "NORMAL"

    def summary(self) -> str:
        """Creates the complete monitoring report."""

        lines = [
            "==========================================",
            "        AQUAGUARD MONITORING REPORT",
            "==========================================",
            "",
            f"Report ID       : {self.report_id}",
            f"Location        : {self.location}",
            f"Location Type   : {self.location.location_type}",
            f"Generated by    : {self.generated_by}",
            f"Generated at    : "
            f"{self.generated_at.strftime('%Y-%m-%d %H:%M')}",
            "",
            f"Status          : {self.status()}",
            f"Total readings  : {len(self.readings)}",
            f"Average use     : "
            f"{self.average_consumption():.1f} litres/day",
            f"Consumption trend: {self.consumption_trend()}",
            "",
            "--------------- READINGS ---------------"
        ]

        for reading in self.readings:
            lines.append(str(reading))

        lines.append("")
        lines.append("---------------- ALERTS ----------------")

        alerts = self.get_all_alerts()

        if alerts:
            for alert in alerts:
                lines.append("• " + alert)
        else:
            lines.append("• No abnormal readings")

        lines.append("")
        lines.append("------------ RECOMMENDATIONS ------------")

        for recommendation in self.recommendations():
            lines.append("• " + recommendation)

        lines.append("")
        lines.append("==========================================")

        return "\n".join(lines)

    def __str__(self):
        return self.summary()


# =========================================================
# DEMO
# =========================================================

if __name__ == "__main__":

    # Create location and user
    loc = Location(
        "House 12B",
        "Green Park Colony",
        "Household"
    )

    user = User(
        "U101",
        "Priya Sharma",
        "Resident"
    )

    # Add daily readings
    r1 = WaterReading(
        date(2026, 9, 10),
        loc,
        user,
        320,
        7.1,
        2.3
    )

    r2 = WaterReading(
        date(2026, 9, 11),
        loc,
        user,
        450,
        6.2,
        6.8
    )

    r3 = WaterReading(
        date(2026, 9, 12),
        loc,
        user,
        510,
        7.4,
        3.1
    )

    # Create monitoring report
    report = MonitoringReport(
        "WR-001",
        user,
        loc
    )

    report.add_reading(r1)
    report.add_reading(r2)
    report.add_reading(r3)

    # Display report
    print(report)
