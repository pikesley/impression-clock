from time import sleep

from lib.clockface import Clockface
from lib.conf import conf
from lib.impression import impression
from lib.timekeeper import Timekeeper

tk = Timekeeper()
cf = Clockface(tk)

while True:
    if tk.has_changed:
        impression.set_image(cf.image, saturation=conf["image-saturation"])
        impression.show()

    tk.update()
    sleep(1)
