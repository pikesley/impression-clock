from PIL import Image, ImageDraw, ImageFont

from lib.conf import conf
from lib.impression import impression

width, height = impression.resolution


class Clockface:
    """Class to generate an image."""

    def __init__(self, keeper, outfile="images/clock.png"):
        """Construct."""
        self.keeper = keeper
        self.width, self.height = impression.resolution
        self.outfile = outfile

    def generate(self):
        """Generate an image."""
        base_image = Image.open(f"backgrounds/{conf['images']['background']}")
        text_image = Image.open(f"backgrounds/{conf['images']['text']}")

        text = Image.new("RGBA", (self.width, self.height), (255, 255, 255, 0))
        self.draw = ImageDraw.Draw(text)

        self.add_text("time")
        self.add_text("date")

        out = Image.composite(text_image, base_image, text)
        out.save(self.outfile)

    @property
    def image(self):  # nocov
        """Get the image."""
        self.generate()
        return Image.open(self.outfile)

    def add_text(self, feature):
        """Add text to the `draw`."""
        self.draw.text(
            (self.centre(feature), conf["features"][feature]["offset"]),
            self.get_feature(feature),
            font=self.font(feature),
        )

    def font(self, feature):
        """Get the font."""
        return ImageFont.truetype(
            f"fonts/{conf['features'][feature]['font']['family']}.ttf",
            conf["features"][feature]["font"]["size"],
        )

    def centre(self, feature):
        """Find the horizontal offset to centre this text."""
        text_width, _ = self.draw.textsize(
            self.get_feature(feature), self.font(feature)
        )
        return (self.width - text_width) / 2

    def get_feature(self, feature_name):
        """Retrieve a thing from our keeper."""
        return getattr(self.keeper, f"{feature_name}_string")
