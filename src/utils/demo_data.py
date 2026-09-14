"""
AquaGuard - Demo Data

Creates representative sample locations and water readings
for demonstrating the AquaGuard monitoring system.
"""

from datetime import date, timedelta

from models.location import LocationUser
from models.water_reading import WaterReading


class DemoDataFactory:
    """Factory for generating realistic demonstration data."""

    @staticmethod
    def create_locations():
        """Create sample monitoring locations."""

        return [
            LocationUser(
                location_id=1,
                name="Green Valley School",
                location_type="School",
                responsible_person="School Water Committee",
                target_daily_liters=900.0,
            ),
            LocationUser(
                location_id=2,
                name="Sunrise Community",
                location_type="Community",
                responsible_person="Community Water Team",
                target_daily_liters=1200.0,
            ),
            LocationUser(
                location_id=3,
                name="Riverside Household",
                location_type="Household",
                responsible_person="Household Member",
                target_daily_liters=600.0,
            ),
            LocationUser(
                location_id=4,
                name="Aqua Public School",
                location_type="School",
                responsible_person="Maintenance Team",
                target_daily_liters=1000.0,
            ),
            LocationUser(
                location_id=5,
                name="Lakeview Community",
                location_type="Community",
                responsible_person="Local Water Committee",
                target_daily_liters=1500.0,
            ),
        ]

    @staticmethod
    def create_readings(
        locations=None,
        days=14,
    ):
        """
        Create sample readings for the supplied locations.

        The dataset intentionally contains:
        - Normal readings
        - High consumption
        - Low/high pH
        - High turbidity
        - Increasing and decreasing usage patterns
        """

        if locations is None:
            locations = (
                DemoDataFactory.create_locations()
            )

        readings = []

        start_date = (
            date.today()
            - timedelta(days=days - 1)
        )

        for location_index, location in enumerate(
            locations
        ):

            for day_index in range(days):

                reading_date = (
                    start_date
                    + timedelta(days=day_index)
                )

                base_consumption = (
                    location.target_daily_liters
                )

                # Different usage patterns for different locations.
                if location_index == 0:
                    # Mostly stable school usage.
                    consumption = (
                        base_consumption
                        + (day_index % 3) * 35
                    )

                elif location_index == 1:
                    # Gradually increasing community usage.
                    consumption = (
                        base_consumption
                        + day_index * 45
                    )

                elif location_index == 2:
                    # Household with decreasing usage.
                    consumption = (
                        base_consumption
                        + 160
                        - day_index * 15
                    )

                elif location_index == 3:
                    # School with occasional excessive usage.
                    consumption = (
                        base_consumption
                        + 40
                    )

                    if day_index in (4, 10):
                        consumption = 1350.0

                else:
                    # Community with moderate variation.
                    consumption = (
                        base_consumption
                        + ((day_index % 4) - 1) * 80
                    )

                ph = 7.1
                turbidity = 1.5
                notes = "Routine monitoring"

                # Add representative abnormal quality readings.
                if location_index == 0 and day_index == 5:
                    ph = 5.9
                    notes = (
                        "Low pH detected during sample check"
                    )

                if location_index == 1 and day_index == 8:
                    turbidity = 7.5
                    notes = (
                        "Elevated turbidity observed"
                    )

                if location_index == 4 and day_index == 11:
                    ph = 9.1
                    turbidity = 6.8
                    notes = (
                        "Multiple abnormal quality indicators"
                    )

                readings.append(
                    WaterReading(
                        reading_id=0,
                        location_id=location.location_id,
                        reading_date=reading_date,
                        consumption_liters=round(
                            consumption,
                            2,
                        ),
                        ph=ph,
                        turbidity_ntu=turbidity,
                        notes=notes,
                    )
                )

        return readings

    @staticmethod
    def create_dataset():
        """
        Create a complete demonstration dataset.

        Returns:
            tuple: (locations, readings)
        """

        locations = (
            DemoDataFactory.create_locations()
        )

        readings = (
            DemoDataFactory.create_readings(
                locations
            )
        )

        return locations, readings
