"""
AquaGuard - Data Exporter

Provides utilities for exporting AquaGuard monitoring
data into CSV format.
"""

import csv
from pathlib import Path


class DataExporter:
    """Exports AquaGuard monitoring data."""

    @staticmethod
    def export_readings(
        file_path,
        locations,
        readings,
    ):
        """
        Export water readings to a CSV file.

        Args:
            file_path: Destination CSV file path.
            locations: Collection of LocationUser objects.
            readings: Collection of WaterReading objects.

        Returns:
            Path: Path of the created CSV file.
        """

        file_path = Path(file_path)

        location_map = {
            location.location_id: location
            for location in locations
        }

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        headers = [
            "Reading ID",
            "Location",
            "Location Type",
            "Date",
            "Consumption (Liters)",
            "pH",
            "Turbidity (NTU)",
            "Quality Status",
            "Consumption Status",
            "Notes",
        ]

        with file_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            writer = csv.writer(
                csv_file
            )

            writer.writerow(
                headers
            )

            for reading in readings:

                location = location_map.get(
                    reading.location_id
                )

                location_name = (
                    location.name
                    if location
                    else "Unknown Location"
                )

                location_type = (
                    location.location_type
                    if location
                    else "Unknown"
                )

                writer.writerow(
                    [
                        reading.reading_id,
                        location_name,
                        location_type,
                        reading.reading_date,
                        f"{reading.consumption_liters:.2f}",
                        f"{reading.ph:.2f}",
                        f"{reading.turbidity_ntu:.2f}",
                        reading.quality_status,
                        reading.consumption_status,
                        reading.notes,
                    ]
                )

        return file_path

    @staticmethod
    def export_summary(
        file_path,
        reports,
    ):
        """
        Export location-wise monitoring summaries.

        Args:
            file_path: Destination CSV file path.
            reports: Collection of MonitoringReport objects.

        Returns:
            Path: Path of the created CSV file.
        """

        file_path = Path(file_path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        headers = [
            "Location",
            "Location Type",
            "Total Consumption (Liters)",
            "Average Consumption (Liters)",
            "Quality Status",
            "Consumption Trend",
            "Alert Count",
        ]

        with file_path.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:

            writer = csv.writer(
                csv_file
            )

            writer.writerow(
                headers
            )

            for report in reports:

                writer.writerow(
                    [
                        report.location.name,
                        report.location.location_type,
                        f"{report.total_consumption:.2f}",
                        f"{report.average_consumption:.2f}",
                        report.quality_status,
                        report.trend,
                        len(report.alerts),
                    ]
                )

        return file_path
