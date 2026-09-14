"""
AquaGuard - Location Model

Defines the LocationUser class used to represent a monitored
household, school, or community location.
"""

from dataclasses import dataclass


@dataclass
class LocationUser:
    """
    Represents a location being monitored by AquaGuard.

    Attributes:
        location_id: Unique identifier for the location.
        name: Name of the household, school, or community.
        location_type: Type of location.
        responsible_person: Person responsible for the location.
        target_daily_liters: Expected daily water consumption target.
    """

    location_id: int
    name: str
    location_type: str
    responsible_person: str
    target_daily_liters: float

    def display_name(self) -> str:
        """Return a user-friendly name for the location."""
        return f"{self.name} ({self.location_type})"

    def is_consumption_target_valid(self, consumption: float) -> bool:
        """
        Check whether a consumption value is within the target.

        Args:
            consumption: Water consumption in liters.

        Returns:
            True if consumption is at or below the target, otherwise False.
        """
        return consumption <= self.target_daily_liters
