class Error(Exception):
    pass


class AlreadyExistsError(Error):
    def __init__(self, message):
        self.message = message


class EmptySongNameError(Error):
    def __init__(self, message):
        self.message = message


class InvalidNameError(Error):
    def __init__(self, message):
        self.message = message


class InvalidEmailError(Error):
    def __init__(self, message):
        self.message = message


class PlaylistNotFoundError(Error):
    def __init__(self, message):
        self.message = message


class PlaylistAlreadyExistsError(Error):
    def __init__(self, message):
        self.message = message


class NotMusicPlaying(Error):
    def __init__(self, message):
        self.message = message


class InvalidVolumeError(Error):
    def __init__(self, message):
        self.message = message


class NotEnoughSongsError(Error):
    def __init__(self, message):
        self.message = message


class ReferencePlaylistNotFoundError(Error):
    def __init__(self, message):
        self.message = message


class SongNotFoundError(Error):
    def __init__(self, message):
        self.message = message
