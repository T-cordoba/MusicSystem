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


class PlaylistNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class PlaylistAlreadyExistsError(Exception):
    def __init__(self, message):
        self.message = message


class NotMusicPlaying(Exception):
    def __init__(self, message):
        self.message = message


class InvalidVolumeError(Exception):
    def __init__(self, message):
        self.message = message


class NotEnoughSongsError(Exception):
    def __init__(self, message):
        self.message = message


class ReferencePlaylistNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class SongNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
