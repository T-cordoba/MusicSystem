import pygame
import random
import json
from pathlib import Path
from sistema_música.exceptions.exceptions import (AlreadyExistsError, EmptySongNameError, PlaylistNotFoundError,
                                                  PlaylistAlreadyExistsError, NotMusicPlaying, InvalidVolumeError,
                                                  NotEnoughSongsError, ReferencePlaylistNotFoundError)


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

    def rename_playlist(self, old_name, new_name):
        if old_name not in self.playlists:
            raise PlaylistNotFoundError(f'No existe una playlist con el nombre {old_name}')
        elif new_name in self.playlists:
            raise PlaylistAlreadyExistsError(f'Ya existe una playlist con el nombre {new_name}')

        for playlist in self.playlists:
            if playlist == old_name:
                self.playlists[new_name] = self.playlists.pop(playlist)
                self.playlists[new_name].name = new_name
                break

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

    def is_music_playing(self):
        return pygame.mixer.music.get_busy()

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
        if self.is_playing:
            self.queue.append(song)
        else:
            raise NotMusicPlaying("No hay música reproduciéndose.")

    def set_volume(self, volume: float):
        self.volume = volume
        if 0 <= self.volume <= 1:
            pygame.mixer.music.set_volume(self.volume)
        else:
            raise InvalidVolumeError("El volumen debe estar entre 0 y 100.")

    def play_playlist(self, playlist: Playlist):
        if playlist.songs:
            first_song = playlist.songs[0]
            self.play(first_song)
            for song in playlist.songs[1:]:
                self.add_to_queue(song)


class SysMusic:
    def __init__(self, audio_player: AudioPlayer):
        self.audio_player = audio_player
        self.songs = self.load_songs()
        self.user = None

    def load_songs(self):
        songs_data_path = (Path(__file__).resolve().parents[2] / 'assets' / 'songs.json')
        with open(songs_data_path, 'r') as f:
            songs_data = json.load(f)

        songs = []
        for song_data in songs_data:
            song = Song(
                song_data['title'],
                song_data['artist'],
                song_data['genre'],
                str((Path(__file__).resolve().parents[2] / 'assets' / str(song_data['file_path'])))
            )
            songs.append(song)

        return songs

    def add_song(self, song: Song):
        for existing_song in self.songs:
            if (existing_song.title == song.title and
                    existing_song.artist == song.artist and existing_song.genre == song.genre):
                raise AlreadyExistsError("La canción ya existe en la lista de canciones.")
        self.songs.append(song)

    def create_random_playlist(self):
        if len(self.songs) < 10:
            raise NotEnoughSongsError("No hay suficientes canciones para crear una lista de reproducción aleatoria.")
        playlist_name = "Random Playlist"
        i = 1
        while playlist_name in self.user.playlists:
            playlist_name = f"Random Playlist {i}"
            i += 1
        random_songs = random.sample(self.songs, 10)
        random_playlist = Playlist(random_songs, playlist_name)
        self.user.playlists[playlist_name] = random_playlist

    def recommend_playlist(self, reference_playlist_name: str):
        if reference_playlist_name not in self.user.playlists:
            raise ReferencePlaylistNotFoundError("Playlist de referencia no encontrada.")
        reference_playlist = self.user.playlists[reference_playlist_name]
        num_songs = min(5, len(reference_playlist.songs))
        sampled_songs = random.sample(reference_playlist.songs, num_songs)
        genres = {song.genre for song in sampled_songs}
        potential_songs = [song for song in self.songs if song.genre in genres and song not in reference_playlist.songs]
        if len(potential_songs) < 10:
            raise NotEnoughSongsError("No hay suficientes canciones para crear una lista de reproducción recomendada.")
        recommended_songs = random.sample(potential_songs, 10)
        playlist_name = f"Playlist recomendada ({', '.join(genres)})"
        recommended_playlist = Playlist(recommended_songs, playlist_name)
        self.user.playlists[playlist_name] = recommended_playlist

        return recommended_playlist

    def remove_song(self, song: Song):
        self.songs.remove(song)

    def set_user(self, user: User):
        self.user = user
