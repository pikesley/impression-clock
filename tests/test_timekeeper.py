from unittest import TestCase

from freezegun import freeze_time

from lib.timekeeper import Timekeeper


class TestTimekeeper(TestCase):
    """Test the Timekeeper."""

    @freeze_time("2020-11-28 22:21")
    def test_constructor(self):
        """Test it has the correct data."""
        tk = Timekeeper()
        self.assertEqual(str(tk.stored_time), "2020-11-28 22:21:00")
        self.assertEqual(tk.time_string, "22:21")
        self.assertEqual(tk.date_string, "28th November")

    @freeze_time("1974-06-15 12:00", as_kwarg="frozen_time")
    def test_changing(self, frozen_time):
        """Test it knows when the time has changed."""
        tk = Timekeeper()

        self.assertEqual(str(tk.stored_time), "1974-06-15 12:00:00")
        self.assertEqual(tk.has_changed, True)

        frozen_time.tick(10)
        tk.update()
        self.assertEqual(tk.has_changed, False)

        frozen_time.tick(50)
        tk.update()
        self.assertEqual(tk.has_changed, True)
        self.assertEqual(str(tk.stored_time), "1974-06-15 12:01:00")
        self.assertEqual(tk.time_string, "12:01")

        frozen_time.tick(1)
        tk.update()
        self.assertEqual(tk.has_changed, False)
