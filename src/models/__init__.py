"""
AquaGuard Models Package

Contains the core data models used by AquaGuard.
"""

from .location import LocationUser
from .water_reading import WaterReading
from .monitoring_report import MonitoringReport

__all__ = [
    "LocationUser",
    "WaterReading",
    "MonitoringReport",
]
