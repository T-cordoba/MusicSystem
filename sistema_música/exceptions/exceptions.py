class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class AlreadyExistsError(Exception):
    def __init__(self, message):
        self.message = message


class EmptySongNameError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidNameError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidEmailError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidAgeError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidOccupationError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidCountryError(Exception):
    def __init__(self, message):
        self.message = message


class PlaylistNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class PlaylistAlreadyExistsError(Exception):
    def __init__(self, message):
        self.message = message
