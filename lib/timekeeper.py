from datetime import datetime


class Timekeeper:
    """Class that knows when the time changes."""

    def __init__(self):
        """Construct."""
        self.has_changed = True
        self.stored_time = datetime.now()

    def update(self):
        """Update the time."""
        previous_time_string = self.time_string

        right_now = datetime.now()
        self.stored_time = right_now
        if previous_time_string != self.time_string:
            self.has_changed = True

        else:
            self.has_changed = False

    @property
    def time_string(self):
        """Time as a string."""
        return self.stored_time.strftime("%H:%M")

    @property
    def date_string(self):
        """Get a date-string."""
        suffixes = {
            1: "st",
            2: "nd",
            3: "rd",
            21: "st",
            22: "nd",
            23: "rd",
            31: "st",
        }

        suffix = suffixes.get(self.stored_time.day, "th")
        return self.stored_time.strftime(f"%-d{suffix} %B")
