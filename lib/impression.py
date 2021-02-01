import platform

if "arm" in platform.platform():  # nocov
    from inky.auto import auto


def imp():
    """Return real or fake impression depending on our platform."""
    if "arm" in platform.platform():
        return auto()  # nocov
    else:
        return FakeImpression()


class FakeImpression:
    """Fake impression for testing."""

    def __init__(self):
        """Construct."""
        self.resolution = (600, 448)

    def set_image(self, image, saturation=1):
        """Set the image."""

    def show(self):
        """Show the image."""


impression = imp()
