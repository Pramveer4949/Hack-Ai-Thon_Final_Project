"""
AquaGuard - Input Validation Utilities

Provides reusable validation functions for water-monitoring
data entered through the application.
"""


class ValidationError(Exception):
    """Raised when user-provided monitoring data is invalid."""

    pass


class InputValidator:
    """Validates AquaGuard input values."""

    @staticmethod
    def validate_name(name):
        """Validate a location or user name."""

        if not name or not name.strip():
            raise ValidationError(
                "Name cannot be empty."
            )

        if len(name.strip()) < 2:
            raise ValidationError(
                "Name must contain at least 2 characters."
            )

        return name.strip()

    @staticmethod
    def validate_location_type(location_type):
        """Validate the selected location type."""

        allowed_types = {
            "Household",
            "School",
            "Community",
        }

        if location_type not in allowed_types:
            raise ValidationError(
                "Please select a valid location type."
            )

        return location_type

    @staticmethod
    def validate_responsible_person(person):
        """Validate the responsible person's name."""

        if not person or not person.strip():
            raise ValidationError(
                "Responsible person cannot be empty."
            )

        return person.strip()

    @staticmethod
    def validate_target_consumption(value):
        """Validate the target daily water consumption."""

        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValidationError(
                "Target consumption must be a number."
            )

        if value <= 0:
            raise ValidationError(
                "Target consumption must be greater than 0."
            )

        return value

    @staticmethod
    def validate_consumption(value):
        """Validate daily water consumption."""

        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValidationError(
                "Daily consumption must be a number."
            )

        if value < 0:
            raise ValidationError(
                "Daily consumption cannot be negative."
            )

        return value

    @staticmethod
    def validate_ph(value):
        """Validate pH input."""

        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValidationError(
                "pH must be a number."
            )

        if value < 0 or value > 14:
            raise ValidationError(
                "pH must be between 0 and 14."
            )

        return value

    @staticmethod
    def validate_turbidity(value):
        """Validate turbidity input."""

        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValidationError(
                "Turbidity must be a number."
            )

        if value < 0:
            raise ValidationError(
                "Turbidity cannot be negative."
            )

        return value

    @staticmethod
    def validate_date(value):
        """Validate that a date value is provided."""

        if value is None:
            raise ValidationError(
                "Reading date is required."
            )

        return value
