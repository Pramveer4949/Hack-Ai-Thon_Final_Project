"""
AquaGuard - Report Generator

Generates human-readable monitoring reports from
AquaGuard MonitoringReport objects.
"""

from datetime import datetime
from pathlib import Path


class ReportGenerator:
    """Generates AquaGuard monitoring reports."""

    @staticmethod
    def generate_text_report(reports):
        """
        Generate a complete text monitoring report.

        Args:
            reports: Collection of MonitoringReport objects.

        Returns:
            str: Formatted monitoring report.
        """

        lines = []

        lines.append("=" * 70)
        lines.append("AQUAGUARD - COMMUNITY WATER MONITORING REPORT")
        lines.append("=" * 70)
        lines.append(
            f"Generated: "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        lines.append("")

        if not reports:
            lines.append(
                "No monitoring data is currently available."
            )
            return "\n".join(lines)

        total_locations = len(reports)
        total_readings = sum(
            len(report.readings)
            for report in reports
        )

        safe_locations = sum(
            1
            for report in reports
            if report.quality_status == "SAFE"
        )

        total_alerts = sum(
            len(report.alerts)
            for report in reports
        )

        lines.append("SYSTEM OVERVIEW")
        lines.append("-" * 70)
        lines.append(
            f"Monitored Locations : {total_locations}"
        )
        lines.append(
            f"Total Readings      : {total_readings}"
        )
        lines.append(
            f"Safe Locations      : {safe_locations}"
        )
        lines.append(
            f"Locations with Issues: "
            f"{total_locations - safe_locations}"
        )
        lines.append(
            f"Total Alerts        : {total_alerts}"
        )
        lines.append("")

        for index, report in enumerate(
            reports,
            start=1,
        ):
            location = report.location

            lines.append("=" * 70)
            lines.append(
                f"LOCATION {index}: {location.name}"
            )
            lines.append("=" * 70)

            lines.append(
                f"Type              : "
                f"{location.location_type}"
            )

            lines.append(
                f"Responsible Person: "
                f"{location.responsible_person}"
            )

            lines.append(
                f"Target Daily Use  : "
                f"{location.target_daily_liters:.2f} L"
            )

            lines.append("")

            lines.append("CONSUMPTION")
            lines.append("-" * 40)

            lines.append(
                f"Total Consumption : "
                f"{report.total_consumption:.2f} L"
            )

            lines.append(
                f"Average Daily Use : "
                f"{report.average_consumption:.2f} L"
            )

            lines.append(
                f"Consumption Trend : "
                f"{report.trend}"
            )

            lines.append("")

            lines.append("WATER QUALITY")
            lines.append("-" * 40)

            lines.append(
                f"Overall Status    : "
                f"{report.quality_status}"
            )

            lines.append("")

            lines.append("ALERTS")
            lines.append("-" * 40)

            if report.alerts:
                for alert in report.alerts:
                    lines.append(
                        f"- {alert}"
                    )
            else:
                lines.append(
                    "No active alerts for this location."
                )

            lines.append("")

            lines.append("RECOMMENDATIONS")
            lines.append("-" * 40)

            if report.recommendations:
                for recommendation in (
                    report.recommendations
                ):
                    lines.append(
                        f"- {recommendation}"
                    )
            else:
                lines.append(
                    "Continue regular monitoring "
                    "and responsible water use."
                )

            lines.append("")

        lines.append("=" * 70)
        lines.append("END OF AQUAGUARD MONITORING REPORT")
        lines.append("=" * 70)

        return "\n".join(lines)

    @staticmethod
    def save_text_report(
        file_path,
        reports,
    ):
        """
        Generate and save a text monitoring report.

        Args:
            file_path: Destination file path.
            reports: Collection of MonitoringReport objects.

        Returns:
            Path: Path of the generated report.
        """

        file_path = Path(file_path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        report_text = (
            ReportGenerator.generate_text_report(
                reports
            )
        )

        file_path.write_text(
            report_text,
            encoding="utf-8",
        )

        return file_path
