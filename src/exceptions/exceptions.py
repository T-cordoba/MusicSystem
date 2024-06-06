class SysMusicError(Exception):
    pass


class AlreadyExistsError(SysMusicError):
    def __init__(self, message):
        self.message = message


class EmptySongNameError(SysMusicError):
    def __init__(self, message):
        self.message = message


class InvalidNameError(SysMusicError):
    def __init__(self, message):
        self.message = message


class InvalidEmailError(SysMusicError):
    def __init__(self, message):
        self.message = message


class PlaylistNotFoundError(SysMusicError):
    def __init__(self, message):
        self.message = message


class PlaylistAlreadyExistsError(SysMusicError):
    def __init__(self, message):
        self.message = message


class NotMusicPlaying(SysMusicError):
    def __init__(self, message):
        self.message = message


class InvalidVolumeError(SysMusicError):
    def __init__(self, message):
        self.message = message


class NotEnoughSongsError(SysMusicError):
    def __init__(self, message):
        self.message = message


class ReferencePlaylistNotFoundError(SysMusicError):
    def __init__(self, message):
        self.message = message


class SongNotFoundError(SysMusicError):
    def __init__(self, message):
        self.message = message
