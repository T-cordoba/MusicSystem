import pygame
import random
import os


class AlreadyExistsError(Exception):
    pass


class EmptySongNameError(Exception):
    pass


class Song:
    def __init__(self, title: str, artist: str, genre: str, file_path: str):
        if title is None:
            raise EmptySongNameError("El nombre de la canción no puede estar vacío.")
        self.title = title
        self.artist = artist
        self.genre = genre
        self.file_path = file_path


class Playlist:
    def __init__(self, songs: list[Song], name: str):
        self.songs = songs
        self.name = name

    def add_song(self, song: Song):
        self.songs.append(song)

    def remove_song(self, song: Song):
        self.songs.remove(song)

    def __str__(self):
        return f"Playlist: {self.name} \nSongs: {self.songs}"


class User:
    def __init__(self, name: str, email: str, age: int, occupation: str, country: str):
        self.name = name
        self.email = email
        self.age = age
        self.occupation = occupation
        self.country = country
        self.playlists: dict[str, Playlist] = {}

    def create_playlist(self, name: str):
        self.playlists[name] = Playlist([], name)

    def delete_playlist(self, name: str):
        del self.playlists[name]

    def add_song_to_playlist(self, song: Song, playlist_name: str):
        self.playlists[playlist_name].add_song(song)

    def remove_song_from_playlist(self, song: Song, playlist_name: str):
        self.playlists[playlist_name].remove_song(song)

    def __str__(self):
        return (f"Nombre: {self.name} \nEmail: {self.email} \nAge: {self.age} \nOccupation: {self.occupation} \n"
                f"Country: {self.country}")


class AudioPlayer:
    def __init__(self, queue: list[Song]):
        self.queue = queue
        self.volume = 0.5
        self.is_playing = False
        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)

    def play(self, song: Song):
        pygame.mixer.music.load(song.file_path)
        pygame.mixer.music.play()
        self.is_playing = True

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        if self.queue:
            next_song = self.queue.pop(0)
            self.play(next_song)

    def add_to_queue(self, song: Song):
        self.queue.append(song)

    def set_volume(self, volume: float):
        self.volume = volume
        if 0 <= self.volume <= 1:
            pygame.mixer.music.set_volume(self.volume)
        else:
            raise ValueError("El volumen debe estar entre 0 y 100.")

    def play_playlist(self, playlist: Playlist):
        if playlist.songs:
            first_song = playlist.songs[0]
            self.play(first_song)
            for song in playlist.songs[1:]:
                self.add_to_queue(song)


class SysMusic:
    def __init__(self, audio_player: AudioPlayer):
        self.audio_player = audio_player
        self.songs: list[Song] = [
            Song('bad guy', 'Billie Eilish', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Billie Eilish - bad guy.mp3')),
            Song('Kiss Me More', 'Doja Cat ft. SZA', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Doja Cat - Kiss Me More.mp3')),
            Song('Levitating', 'Dua Lipa', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Dua Lipa - Levitating.mp3')),
            Song('Shape of You', 'Ed Sheeran', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Ed Sheeran - Shape of You.mp3')),
            Song('As it was', 'Harry Styles', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Harry Styles - As It Was.mp3')),
            Song('Roar', 'Katy Perry', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Katy Perry - Roar.mp3')),
            Song('Bad Romance', 'Lady Gaga', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Lady Gaga - Bad Romance.mp3')),
            Song('Sugar', 'Maroon 5', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Maroon 5 - Sugar.mp3')),
            Song('Billie Jean', 'Michael Jackson', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Michael Jackson - Billie Jean.mp3')),
            Song('good 4 u', 'Olivia Rodrigo', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Olivia Rodrigo - good 4 u.mp3')),
            Song('Sunflower', 'Post Malone ft. Swae Lee', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Post Malone & Swae Lee - Sunflower.mp3')),
            Song('Bohemian Rhapsody', 'Queen', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Queen - Bohemian Rhapsody.mp3')),
            Song('Leave the Door Open', 'Silk Sonic', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Silk Sonic - Leave the Door Open.mp3')),
            Song('Blank Space', 'Taylor Swift', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Taylor Swift - Blank Space.mp3')),
            Song('Blinding Lights', 'The Weeknd', 'Pop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'The Weeknd - Blinding Lights.mp3')),
            Song('Back in Black', 'AC/DC', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'ACDC - Back in Black.mp3')),
            Song('Sweet Child O Mine', 'Guns N Roses', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Guns N Roses - Sweet Child o Mine.mp3')),
            Song('Smells Like Teen Spirit', 'Nirvana', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Nirvana - Smells Like Teen Spirit.mp3')),
            Song('Radioactive', 'Imagine Dragons', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Imagine Dragons - Radioactive.mp3')),
            Song('Everlong', 'Foo Fighters', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Foo Fighters - Everlong.mp3')),
            Song('In the End', 'Linkin Park', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Linkin Park - In the End.mp3')),
            Song('Stairway to Heaven', 'Led Zeppelin', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Led Zeppelin - Stairway to Heaven.mp3')),
            Song('Enter Sandman', 'Metallica', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Metallica - Enter Sandman.mp3')),
            Song('Hey Jude', 'The Beatles', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'The Beatles - Hey Jude.mp3')),
            Song('Wish You Were Here', 'Pink Floyd', 'Rock',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Pink Floyd - Wish You Were Here.mp3')),
            Song('One more time', 'Daft Punk', 'Electronica',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Daft Punk - One More Time.mp3')),
            Song('Feel so close', 'Calvin Harris', 'Electronica',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Calvin Harris - Feel So Close.mp3')),
            Song('Wake me up', 'Avicii', 'Electronica',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Avicii - Wake Me Up.mp3')),
            Song('Dont you worry child', 'Swedish House Mafia', 'Electronica',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Swedish House Mafia - Dont You Worry Child.mp3')),
            Song('Animals', 'Martin Garrix', 'Electronica',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Martin Garrix - Animals.mp3')),
            Song('Ghost n Stuff', 'Deadmau5', 'Electronica',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Deadmau5 - Ghosts n Stuff.mp3')),
            Song('D.A.N.C.E.', 'Justice', 'Electronica',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Justice - D.A.N.C.E..mp3')),
            Song('Galvanize', 'The Chemical Brothers', 'Electronica',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'The Chemical Brothers - Galvanize.mp3')),
            Song('HUMBLE.', 'Kendrick Lamar', 'Hip Hop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Kendrick Lamar - HUMBLE..mp3')),
            Song('Gods Plan', 'Drake', 'Hip Hop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Drake - Gods Plan.mp3')),
            Song('Stronger', 'Kanye West', 'Hip Hop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Kanye West - Stronger.mp3')),
            Song('Lose Yourself', 'Eminem', 'Hip Hop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Eminem - Lose Yourself.mp3')),
            Song('Empire State of Mind', 'Jay Z ft. Alicia', 'Hip Hop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Jay-Z - Empire State of Mind.mp3')),
            Song('Changes', '2Pac', 'Hip Hop',
                 os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets',
                              'Tupac Shakur - Changes.mp3')),
        ]
        self.user = None

    def add_song(self, song: Song):
        for existing_song in self.songs:
            if existing_song.title == song.title and existing_song.artist == song.artist and existing_song.genre == song.genre:
                raise AlreadyExistsError("La canción ya existe en la lista de canciones.")
        self.songs.append(song)

    def create_random_playlist(self):
        if len(self.songs) < 10:
            raise ValueError("No hay suficientes canciones para crear una lista de reproducción aleatoria.")
        i=0
        random_songs = random.sample(self.songs, 10)
        random_playlist = Playlist(random_songs, "Random Playlist")


    def remove_song(self, song: Song):
        self.songs.remove(song)

    def set_user(self, user: User):
        self.user = user



