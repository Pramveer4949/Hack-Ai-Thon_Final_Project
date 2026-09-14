"""
AquaGuard - Analytics Engine

Provides calculations and analysis for water consumption,
water quality, alerts, trends, and conservation performance.
"""

from statistics import mean

from models.location import LocationUser
from models.monitoring_report import MonitoringReport
from models.water_reading import WaterReading


class AnalyticsEngine:
    """Performs analytics on AquaGuard monitoring data."""

    def __init__(
        self,
        locations: list[LocationUser],
        readings: list[WaterReading],
    ):
        """
        Initialize the analytics engine.

        Args:
            locations: List of monitored locations.
            readings: List of water readings.
        """

        self.locations = locations
        self.readings = readings

    def get_location_readings(
        self,
        location_id: int,
    ) -> list[WaterReading]:
        """Return readings belonging to a specific location."""

        return [
            reading
            for reading in self.readings
            if reading.location_id == location_id
        ]

    def get_location(
        self,
        location_id: int,
    ) -> LocationUser | None:
        """Return a location by ID."""

        for location in self.locations:
            if location.location_id == location_id:
                return location

        return None

    def generate_report(
        self,
        location_id: int,
    ) -> MonitoringReport | None:
        """Generate a monitoring report for one location."""

        location = self.get_location(location_id)

        if location is None:
            return None

        readings = self.get_location_readings(location_id)

        return MonitoringReport(
            location=location,
            readings=readings,
        )

    def generate_all_reports(self) -> list[MonitoringReport]:
        """Generate reports for every monitored location."""

        reports = []

        for location in self.locations:
            report = self.generate_report(location.location_id)

            if report is not None:
                reports.append(report)

        return reports

    def total_consumption(self) -> float:
        """Return total water consumption across all readings."""

        return sum(
            reading.consumption_liters
            for reading in self.readings
        )

    def average_consumption(self) -> float:
        """Return average consumption across all readings."""

        if not self.readings:
            return 0.0

        return mean(
            reading.consumption_liters
            for reading in self.readings
        )

    def safe_reading_count(self) -> int:
        """Return the number of readings with safe water quality."""

        return sum(
            reading.quality_status == "Safe"
            for reading in self.readings
        )

    def unsafe_reading_count(self) -> int:
        """Return the number of readings with unsafe water quality."""

        return sum(
            reading.quality_status == "Unsafe"
            for reading in self.readings
        )

    def excessive_consumption_count(self) -> int:
        """Return the number of readings with excessive consumption."""

        return sum(
            reading.consumption_status == "Excessive"
            for reading in self.readings
        )

    def active_alert_count(self) -> int:
        """Return the total number of generated alerts."""

        return sum(
            len(reading.alert_messages())
            for reading in self.readings
        )

    def overall_quality(self) -> str:
        """Return the overall quality status of the monitored system."""

        if not self.readings:
            return "No Data"

        if self.unsafe_reading_count() > 0:
            return "Unsafe"

        return "Safe"

    def conservation_score(self) -> float:
        """
        Calculate a simple conservation score.

        The score is based on how many readings stayed within
        the configured daily consumption threshold.

        Returns:
            A percentage from 0 to 100.
        """

        if not self.readings:
            return 0.0

        normal_readings = sum(
            reading.consumption_status == "Normal"
            for reading in self.readings
        )

        return round(
            (normal_readings / len(self.readings)) * 100,
            1,
        )

    def quality_score(self) -> float:
        """
        Calculate the percentage of readings with safe quality.

        Returns:
            A percentage from 0 to 100.
        """

        if not self.readings:
            return 0.0

        safe_readings = self.safe_reading_count()

        return round(
            (safe_readings / len(self.readings)) * 100,
            1,
        )

    def location_summary(self) -> list[dict]:
        """Return a location-wise analytical summary."""

        summaries = []

        for report in self.generate_all_reports():
            summaries.append(
                {
                    "location_id": report.location.location_id,
                    "location": report.location.name,
                    "type": report.location.location_type,
                    "average_consumption": round(
                        report.average_consumption,
                        2,
                    ),
                    "quality_status": report.quality_status,
                    "trend": report.trend,
                    "alerts": len(report.alerts),
                    "conservation_status": report.conservation_status,
                }
            )

        return summaries

    def dashboard_summary(self) -> dict:
        """Return the main values required by the dashboard."""

        return {
            "locations": len(self.locations),
            "readings": len(self.readings),
            "total_consumption": round(
                self.total_consumption(),
                2,
            ),
            "average_consumption": round(
                self.average_consumption(),
                2,
            ),
            "quality_score": self.quality_score(),
            "conservation_score": self.conservation_score(),
            "active_alerts": self.active_alert_count(),
            "overall_quality": self.overall_quality(),
        }

    def get_consumption_trend(
        self,
        location_id: int | None = None,
    ) -> list[tuple]:
        """
        Return consumption data suitable for a trend chart.

        Args:
            location_id: Optional location filter.

        Returns:
            List of (date, consumption) tuples.
        """

        if location_id is None:
            selected_readings = self.readings
        else:
            selected_readings = self.get_location_readings(
                location_id
            )

        ordered_readings = sorted(
            selected_readings,
            key=lambda reading: reading.reading_date,
        )

        return [
            (
                reading.reading_date,
                reading.consumption_liters,
            )
            for reading in ordered_readings
        ]

    def get_quality_breakdown(self) -> dict:
        """Return counts of safe and unsafe readings."""

        safe = self.safe_reading_count()
        unsafe = self.unsafe_reading_count()

        return {
            "Safe": safe,
            "Unsafe": unsafe,
        }
