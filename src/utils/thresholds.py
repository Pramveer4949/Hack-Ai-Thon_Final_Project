"""
AquaGuard - Monitoring Thresholds

Centralized configuration for water-quality and
water-consumption monitoring limits.
"""


class ThresholdManager:
    """Stores and manages AquaGuard monitoring thresholds."""

    PH_MIN = 6.5
    PH_MAX = 8.5

    TURBIDITY_MAX = 5.0

    DAILY_CONSUMPTION_ALERT = 1000.0

    @classmethod
    def get_all(cls):
        """Return all configured thresholds."""

        return {
            "ph_min": cls.PH_MIN,
            "ph_max": cls.PH_MAX,
            "turbidity_max": cls.TURBIDITY_MAX,
            "consumption_alert": cls.DAILY_CONSUMPTION_ALERT,
        }

    @classmethod
    def is_ph_safe(cls, ph):
        """Check whether a pH value is within the configured range."""

        return cls.PH_MIN <= ph <= cls.PH_MAX

    @classmethod
    def is_turbidity_safe(cls, turbidity):
        """Check whether turbidity is within the configured limit."""

        return turbidity <= cls.TURBIDITY_MAX

    @classmethod
    def is_consumption_excessive(cls, consumption):
        """Check whether daily consumption is excessive."""

        return consumption > cls.DAILY_CONSUMPTION_ALERT

    @classmethod
    def quality_status(cls, ph, turbidity):
        """Return the overall quality status for a reading."""

        if not cls.is_ph_safe(ph):
            return "UNSAFE"

        if not cls.is_turbidity_safe(turbidity):
            return "UNSAFE"

        return "SAFE"

    @classmethod
    def consumption_status(cls, consumption):
        """Return the consumption status."""

        if cls.is_consumption_excessive(consumption):
            return "EXCESSIVE"

        return "NORMAL"
