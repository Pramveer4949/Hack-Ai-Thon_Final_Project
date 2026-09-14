"""
AquaGuard GUI package.

Contains the graphical user interface components for the
AquaGuard water quality and usage monitoring system.
"""

from .main_window import MainWindow
from .dashboard import Dashboard
from .add_reading import AddReadingPage
from .analytics_page import AnalyticsPage
from .alerts_page import AlertsPage
from .locations_page import LocationsPage
from .monitoring_report_page import MonitoringReportPage
from .thresholds_page import ThresholdsPage

__all__ = [
    "MainWindow",
    "Dashboard",
    "AddReadingPage",
    "AnalyticsPage",
    "AlertsPage",
    "LocationsPage",
    "MonitoringReportPage",
    "ThresholdsPage",
]
