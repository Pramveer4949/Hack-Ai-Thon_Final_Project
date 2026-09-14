"""
AquaGuard - Database Manager

Handles SQLite database creation and storage for locations
and water-monitoring readings.
"""

import sqlite3
from datetime import date
from pathlib import Path

from models.location import LocationUser
from models.water_reading import WaterReading


class DatabaseManager:
    """Manages AquaGuard's SQLite database."""

    def __init__(self, database_path: str | None = None):
        """
        Initialize the database manager.

        Args:
            database_path: Optional path to the SQLite database.
        """

        if database_path is None:
            project_root = Path(__file__).resolve().parents[2]
            database_path = project_root / "aquaguard.db"

        self.database_path = str(database_path)

        self.initialize()

    def connect(self):
        """Create and return a database connection."""

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self):
        """Create required database tables if they do not exist."""

        with self.connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS locations (
                    location_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location_type TEXT NOT NULL,
                    responsible_person TEXT NOT NULL,
                    target_daily_liters REAL NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS readings (
                    reading_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location_id INTEGER NOT NULL,
                    reading_date TEXT NOT NULL,
                    consumption_liters REAL NOT NULL,
                    ph REAL NOT NULL,
                    turbidity_ntu REAL NOT NULL,
                    notes TEXT DEFAULT '',
                    FOREIGN KEY (location_id)
                        REFERENCES locations(location_id)
                        ON DELETE CASCADE
                )
                """
            )

            connection.commit()

    def add_location(self, location: LocationUser) -> int:
        """
        Add a new monitored location.

        Returns:
            The generated database ID.
        """

        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO locations (
                    name,
                    location_type,
                    responsible_person,
                    target_daily_liters
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    location.name,
                    location.location_type,
                    location.responsible_person,
                    location.target_daily_liters,
                ),
            )

            connection.commit()
            return cursor.lastrowid

    def get_locations(self) -> list[LocationUser]:
        """Return all monitored locations."""

        with self.connect() as connection:
            rows = connection.execute(
                """
                SELECT
                    location_id,
                    name,
                    location_type,
                    responsible_person,
                    target_daily_liters
                FROM locations
                ORDER BY name
                """
            ).fetchall()

        return [
            LocationUser(
                location_id=row["location_id"],
                name=row["name"],
                location_type=row["location_type"],
                responsible_person=row["responsible_person"],
                target_daily_liters=row["target_daily_liters"],
            )
            for row in rows
        ]

    def get_location(self, location_id: int) -> LocationUser | None:
        """Return one location by its ID."""

        with self.connect() as connection:
            row = connection.execute(
                """
                SELECT
                    location_id,
                    name,
                    location_type,
                    responsible_person,
                    target_daily_liters
                FROM locations
                WHERE location_id = ?
                """,
                (location_id,),
            ).fetchone()

        if row is None:
            return None

        return LocationUser(
            location_id=row["location_id"],
            name=row["name"],
            location_type=row["location_type"],
            responsible_person=row["responsible_person"],
            target_daily_liters=row["target_daily_liters"],
        )

    def add_reading(self, reading: WaterReading) -> int:
        """
        Add a new water reading.

        Returns:
            The generated database ID.
        """

        with self.connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO readings (
                    location_id,
                    reading_date,
                    consumption_liters,
                    ph,
                    turbidity_ntu,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    reading.location_id,
                    reading.reading_date.isoformat(),
                    reading.consumption_liters,
                    reading.ph,
                    reading.turbidity_ntu,
                    reading.notes,
                ),
            )

            connection.commit()
            return cursor.lastrowid

    def get_readings(
        self,
        location_id: int | None = None,
    ) -> list[WaterReading]:
        """
        Return water readings.

        Args:
            location_id: If provided, return readings only for that location.
        """

        with self.connect() as connection:

            if location_id is None:
                rows = connection.execute(
                    """
                    SELECT
                        reading_id,
                        location_id,
                        reading_date,
                        consumption_liters,
                        ph,
                        turbidity_ntu,
                        notes
                    FROM readings
                    ORDER BY reading_date
                    """
                ).fetchall()

            else:
                rows = connection.execute(
                    """
                    SELECT
                        reading_id,
                        location_id,
                        reading_date,
                        consumption_liters,
                        ph,
                        turbidity_ntu,
                        notes
                    FROM readings
                    WHERE location_id = ?
                    ORDER BY reading_date
                    """,
                    (location_id,),
                ).fetchall()

        return [
            WaterReading(
                reading_id=row["reading_id"],
                location_id=row["location_id"],
                reading_date=date.fromisoformat(row["reading_date"]),
                consumption_liters=row["consumption_liters"],
                ph=row["ph"],
                turbidity_ntu=row["turbidity_ntu"],
                notes=row["notes"] or "",
            )
            for row in rows
        ]

    def delete_all_data(self):
        """Delete all stored locations and readings."""

        with self.connect() as connection:
            connection.execute("DELETE FROM readings")
            connection.execute("DELETE FROM locations")
            connection.commit()

    def location_count(self) -> int:
        """Return the number of monitored locations."""

        with self.connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM locations"
            ).fetchone()

        return row["count"]

    def reading_count(self) -> int:
        """Return the total number of stored water readings."""

        with self.connect() as connection:
            row = connection.execute(
                "SELECT COUNT(*) AS count FROM readings"
            ).fetchone()

        return row["count"]
