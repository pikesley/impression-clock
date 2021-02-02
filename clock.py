from time import sleep

from lib.clockface import Clockface
from lib.conf import conf
from lib.impression import impression
from lib.timekeeper import Timekeeper

keeper = Timekeeper()
cf = Clockface(keeper)

while True:
    if keeper.has_changed:
        impression.set_image(cf.image, saturation=conf["image-saturation"])
        impression.show()

    keeper.update()
    sleep(1)
