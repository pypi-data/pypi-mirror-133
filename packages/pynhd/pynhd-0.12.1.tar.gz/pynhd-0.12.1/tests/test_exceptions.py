import pytest

from pynhd import InvalidInputRange, MissingItems


def missing_items():
    raise MissingItems(["tmin", "dayl"])


def test_missing_items():
    with pytest.raises(MissingItems):
        missing_items()
