from lib.impression import impression


def test_impression():
    """Test we get a testable board."""
    assert impression.resolution == (600, 448)
    assert hasattr(impression, "set_image")
    assert hasattr(impression, "show")
