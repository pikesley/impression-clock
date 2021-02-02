from hashlib import sha256
from pathlib import Path
from unittest import TestCase

from freezegun import freeze_time

from lib.clockface import Clockface
from lib.timekeeper import Timekeeper

checksums = {
    "12:34": "9e4a477ed76940e3cba27b5f3e0cade6c750be7f14ec7bb26fa2ee9c44c9529b",
    "12:35": "01234cbdebc0568a938254854bf851e406f65f40102a9f70e845bd451664c925",
}


class TestClockface(TestCase):
    """Test the Clockface."""

    @freeze_time("1974-06-15 12:34:56", as_kwarg="frozen_time")
    def test_image_generation(self, frozen_time):
        """Test it creates the image we expect."""
        Path("tmp/").mkdir(exist_ok=True)
        keeper = Timekeeper()
        face = Clockface(keeper, outfile="tmp/clock.png")
        face.generate()

        checksum = sha256(Path("tmp/clock.png").read_bytes()).hexdigest()
        assert checksum == checksums["12:34"]

        frozen_time.tick(60)
        keeper.update()
        face.generate()
        checksum = sha256(Path("tmp/clock.png").read_bytes()).hexdigest()
        assert checksum == checksums["12:35"]
