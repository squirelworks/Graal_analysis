"""Errors for the level conversion chain."""


class ConvertError(Exception):
    """The file is the wrong shape, or the conversion cannot be done."""


class Truncated(ConvertError):
    """The file ends before a section the format says is still open."""
