from freezegun import freeze_time

from lib.clockface import Clockface
from lib.timekeeper import Timekeeper


def test_generate_large_face():
    outfile = "tmp/test-font-size.png"
    with freeze_time("2021-09-22 00:00"):
        tk = Timekeeper()
        cf = Clockface(tk, outfile)
        cf.generate()
