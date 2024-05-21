import PySimpleGUI as sg
from pathlib import Path
from sistema_música.model.sis_música import Song, User, SysMusic
from sistema_música.exceptions.exceptions import (InvalidNameError, InvalidEmailError, InvalidAgeError,
                                                  InvalidOccupationError, InvalidCountryError)


class SysMusicGUI:
    sg.theme('DarkAmber')

    def __init__(self, sys_music: SysMusic):
        self.sys_music = sys_music

    def start_menu_gui(self):
        layout = [
                [sg.Text('Sistema de música', font=('Book', 20))],
                [sg.Image(str((Path(__file__).resolve().parents[2] / 'assets' / 'music_icon.png')),
                          subsample=4)],
                [sg.Text('')],
                [sg.Button('Iniciar', size=(8, 2), border_width=0), sg.Button('Salir', size=(8, 2), border_width=0)]
        ]
        window = sg.Window('Sistema de música', layout, element_justification='c', finalize=True)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Salir':
                break
            if event == 'Iniciar':
                window.close()
                self.user_info_gui()
                self.music_player_gui()
        window.close()

    def user_info_gui(self):
        while True:
            layout = [
                [sg.Text('Ingrese su nombre:'), sg.InputText(key='-NAME-', expand_x=True, size=(5, 1))],
                [sg.Text('Ingrese su email:'), sg.InputText(key='-EMAIL-', expand_x=True, size=(5, 1))],
                [sg.Text('Ingrese su edad:'), sg.InputText(key='-AGE-', expand_x=True, size=(5, 1))],
                [sg.Text('Ingrese su ocupación:'), sg.InputText(key='-OCCUPATION-', expand_x=True, size=(5, 1))],
                [sg.Text('Ingrese su país:'), sg.InputText(key='-COUNTRY-', expand_x=True, size=(5, 1))],
                [sg.Button('Ok', border_width=0, size=(8, 1))]
            ]
            window = sg.Window('Información del usuario', layout, element_justification='c', resizable=True,
                               margins=(15, 10))
            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED:
                    exit()
                elif event == 'Ok':
                    name = values['-NAME-']
                    email = values['-EMAIL-']
                    age = values['-AGE-']
                    occupation = values['-OCCUPATION-']
                    country = values['-COUNTRY-']
                    try:
                        if not name.isalpha():
                            raise InvalidNameError("El nombre solo puede contener letras")
                        if "@" not in email or "." not in email:
                            raise InvalidEmailError("El email debe contener @ y .")
                        if not age.isdigit() or not (1 <= int(age) <= 100):
                            raise InvalidAgeError("La edad debe ser un número entre 1 y 100")
                        if not occupation.isalpha():
                            raise InvalidOccupationError("La ocupación solo puede contener letras")
                        if not country.isalpha():
                            raise InvalidCountryError("El país solo puede contener letras")
                        self.sys_music.user = User(name, email, int(age), occupation, country)
                        window.close()
                        return
                    except (InvalidNameError, InvalidEmailError, InvalidAgeError, InvalidOccupationError,
                            InvalidCountryError) as e:
                        sg.popup(str(e))
                        break
            window.close()

    def add_song_gui(self, file_path):
        layout = [
            [sg.Text(f'Dirección del archivo: {file_path}')],
            [sg.Text('Titulo:'), sg.InputText(key='-TITLE-')],
            [sg.Text('Artista:'), sg.InputText(key='-ARTIST-')],
            [sg.Text('Genero:'), sg.InputText(key='-GENRE-')],
            [sg.Button('OK', border_width=0), sg.Button('Cancelar', border_width=0)]
        ]
        window = sg.Window('Añadir canción', layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                return None
            elif event == 'OK':
                break
        window.close()
        return {**values, '-FILEPATH-': file_path}

    def create_playlist_gui(self):
        layout = [
            [sg.Text('Nombre de la playlist:'), sg.InputText(key='-NAME-')],
            [sg.Button('OK', border_width=0)]
        ]
        window = sg.Window('Crear playlist', layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == 'OK':
                playlist_name = values['-NAME-']
                self.sys_music.user.create_playlist(playlist_name)
                break
        window.close()

    def rename_playlist_gui(self, playlist_name):
        layout = [
            [sg.Text(playlist_name, key='-PLAYLIST NAME-')],
            [sg.Text('Nuevo nombre:'), sg.InputText(key='-NEW NAME-')],
            [sg.Button('OK', border_width=0)]
        ]
        window = sg.Window('Renombrar playlist', layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                break
            if event == 'OK':
                try:
                    self.sys_music.user.rename_playlist(playlist_name, values['-NEW NAME-'])
                except Exception as e:
                    sg.popup(e)
                break
        window.close()

    def see_playlist_gui(self, playlist_name):
        playlist = self.sys_music.user.playlists[playlist_name]
        song_list = [f"{song.title} - {song.artist} - {song.genre}" for song in playlist.songs]

        layout = [
            [sg.Text(f'Playlist: {playlist_name}')],
            [sg.Text('Canciones en la playlist:')],
            [sg.Listbox(values=song_list, size=(50, 20), key='-SONG LIST-')],
            [sg.Button('Añadir canción', border_width=0), sg.Button('Eliminar canción', border_width=0)],
            [sg.Text('Canciones disponibles:')],
            [sg.Listbox(values=[f"{song.title} - {song.artist} - {song.genre}" for song in self.sys_music.songs],
                        size=(50, 10), key='-SONG LIST AVAILABLE-')],
            [sg.Button('OK', border_width=0)]
        ]

        window = sg.Window('Ver playlist', layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'OK':
                break
            elif event == 'Añadir canción':
                if values['-SONG LIST AVAILABLE-']:
                    selected_song_details = values['-SONG LIST AVAILABLE-'][0].split(' - ')
                    for song in self.sys_music.songs:
                        if [song.title, song.artist, song.genre] == selected_song_details:
                            self.sys_music.user.add_song_to_playlist(song, playlist_name)
                            playlist = self.sys_music.user.playlists[playlist_name]
                            window['-SONG LIST-'].update(
                                [f"{song.title} - {song.artist} - {song.genre}" for song in playlist.songs])
                            break
                else:
                    sg.popup('Por favor, selecciona una canción antes de presionar añadir canción')
            elif event == 'Eliminar canción':
                if values['-SONG LIST-']:
                    selected_song_details = values['-SONG LIST-'][0].split(' - ')
                    for song in playlist.songs:
                        if [song.title, song.artist, song.genre] == selected_song_details:
                            self.sys_music.user.remove_song_from_playlist(song, playlist_name)
                            playlist = self.sys_music.user.playlists[playlist_name]
                            window['-SONG LIST-'].update(
                                [f"{song.title} - {song.artist} - {song.genre}" for song in playlist.songs])
                            break
                else:
                    sg.popup('Por favor, selecciona una canción antes de presionar eliminar canción')

        window.close()

    def music_player_gui(self):
        try:
            user_name = self.sys_music.user.name
        except AttributeError:
            sg.popup('Por favor, ingrese su información de usuario antes de continuar')
            return
        layout = [
            [sg.Button('Información del usuario', tooltip='Muestra la información del usuario', border_width=0)],
            [sg.Text(f'Hola, {user_name}')],
            [sg.Text('')],
            [sg.Input(key='-FILE-', visible=False, enable_events=True),
             sg.FileBrowse(file_types=(("MP3 Files", "*.mp3"), ), button_text='Añadir canción',
                           tooltip='Agrega un archivo de música al sistema')],
            [sg.Text('Canciones disponibles:'), sg.Text('                                                     '),
             sg.Text('Canciones en la cola:')],
            [sg.Listbox(values=[], size=(50, 2), key='-SONG LIST-', bind_return_key=True, expand_y=True),
             sg.Listbox(values=[], size=(50, 2), key='-QUEUE-', bind_return_key=True, expand_y=True,
                        justification='right')],
            [sg.Button('Editar', tooltip='Edita la información de la canción seleccionada', border_width=0),
             sg.Button('Eliminar', tooltip='Elimina la canción seleccionada', border_width=0)],
            [sg.Text('')],
            [sg.Text('Playlists del usuario:')],
            [sg.Listbox(values=[], size=(50, 2), key='-PLAYLIST LIST-', bind_return_key=True, expand_y=True)],
            [sg.Button('Crear playlist', tooltip='Crea una playlist', border_width=0),
             sg.Button('Eliminar playlist', tooltip='Elimina la playlist seleccionada', border_width=0),
             sg.Button('Renombrar playlist', tooltip='Renombra la playlist seleccionada', border_width=0),
             sg.Button('Ver playlist', tooltip='Muestra y edita las canciones de la playlist seleccionada',
                       border_width=0)],
            [sg.Button('Crear playlist aleatoria', tooltip='Crea una playlist aleatoria', border_width=0),
             sg.Button('Recomendar playlist',
                       tooltip='Recomienda una playlist con generos similares a la playlist seleccionada',
                       border_width=0)],
            [sg.Button('Reproducir playlist', tooltip='Reproducir la playlist seleccionada', border_width=0)],
            [sg.Text('')],
            [sg.Text('Volumen:')],
            [sg.Slider(range=(0, 100), orientation='horizontal', size=(20, 10), key='-VOLUME SLIDER-',
                       default_value=50)],
            [sg.Text('')],
            [sg.Button('Reproducir'), sg.Button('Pausar'), sg.Button('Parar'), sg.Button('Siguiente'),
             sg.Button('Añadir a la cola')]
        ]
        window = sg.Window('Sistema de música', layout, finalize=True, resizable=True)
        window['-SONG LIST-'].update(
            [f"{song.title} - {song.artist} - {song.genre}" for song in self.sys_music.songs])
        paused = False
        while True:
            event, values = window.read(timeout=100)
            if event == sg.WINDOW_CLOSED:
                break
            if event == '-FILE-':
                song_file_path = values['-FILE-'].split(';')[0]
                song_details = self.add_song_gui(song_file_path)
                if song_details is not None:
                    song = Song(song_details['-TITLE-'], song_details['-ARTIST-'], song_details['-GENRE-'],
                                song_file_path)
                    try:
                        self.sys_music.add_song(song)
                    except Exception as e:
                        sg.popup(str(e))
                    window['-SONG LIST-'].update(
                        [f"{song.title} - {song.artist} - {song.genre}" for song in self.sys_music.songs])
            elif event == sg.TIMEOUT_EVENT:
                self.sys_music.audio_player.set_volume(int(values['-VOLUME SLIDER-']) / 100)

                if not self.sys_music.audio_player.is_music_playing():
                    self.sys_music.audio_player.next()
                    window['-QUEUE-'].update(
                        [f"{song.title} - {song.artist} - {song.genre}" for song in
                         self.sys_music.audio_player.queue])
            elif event == 'Reproducir':
                if values['-SONG LIST-']:
                    window['Pausar'].update('Pausar')
                    paused = False
                    selected_song_details = values['-SONG LIST-'][0].split(' - ')
                    for song in self.sys_music.songs:
                        if [song.title, song.artist, song.genre] == selected_song_details:
                            self.sys_music.audio_player.play(song)
                            break
                else:
                    sg.popup('Por favor, selecciona una canción antes de presionar reproducir')
            elif event == 'Pausar':
                if self.sys_music.audio_player.is_playing:
                    if paused:
                        self.sys_music.audio_player.unpause()
                        window['Pausar'].update('Pausar')
                        paused = False
                    else:
                        self.sys_music.audio_player.pause()
                        window['Pausar'].update('Despausar')
                        paused = True
                else:
                    sg.popup('No hay canciones para pausar')
            elif event == 'Parar':
                if self.sys_music.audio_player.is_playing:
                    window['Pausar'].update('Pausar')
                    paused = False
                    self.sys_music.audio_player.stop()
                else:
                    sg.popup('No hay canciones para parar')
            elif event == 'Editar':
                if values['-SONG LIST-']:
                    self.sys_music.audio_player.stop()
                    window['Pausar'].update('Pausar')
                    paused = False
                    selected_song_file_paths = values['-SONG LIST-']
                    for song in self.sys_music.songs:
                        if f"{song.title} - {song.artist} - {song.genre}" in selected_song_file_paths:
                            self.edit_song_gui(song)
                            window['-SONG LIST-'].update(
                                [f"{song.title} - {song.artist} - {song.genre}" for song in self.sys_music.songs])
                            break
                else:
                    sg.popup('Por favor, selecciona una canción antes de presionar editar')
            elif event == 'Eliminar':
                if values['-SONG LIST-']:
                    self.sys_music.audio_player.stop()
                    window['Pausar'].update('Pausar')
                    paused = False
                    selected_song_details = values['-SONG LIST-'][0].split(' - ')
                    for song in self.sys_music.songs:
                        if [song.title, song.artist, song.genre] == selected_song_details:
                            self.sys_music.remove_song(song)
                            window['-SONG LIST-'].update(
                                [f"{song.title} - {song.artist} - {song.genre}" for song in self.sys_music.songs])
                            break
                else:
                    sg.popup('Por favor, selecciona una canción antes de presionar eliminar')
            elif event == 'Información del usuario':
                sg.popup(str(self.sys_music.user))
            elif event == 'Crear playlist':
                self.create_playlist_gui()
                window['-PLAYLIST LIST-'].update(
                    [playlist.name for playlist in self.sys_music.user.playlists.values()])
            elif event == 'Eliminar playlist':
                if values['-PLAYLIST LIST-']:
                    selected_playlist = values['-PLAYLIST LIST-'][0]
                    self.sys_music.user.delete_playlist(selected_playlist)
                    window['-PLAYLIST LIST-'].update(
                        [playlist.name for playlist in self.sys_music.user.playlists.values()])
                else:
                    sg.popup('Por favor, selecciona una playlist antes de presionar eliminar')
            elif event == 'Ver playlist':
                if values['-PLAYLIST LIST-']:
                    selected_playlist = values['-PLAYLIST LIST-'][0]
                    self.see_playlist_gui(selected_playlist)
                else:
                    sg.popup('Por favor, selecciona una playlist antes de presionar Ver playlist')
            elif event == 'Reproducir playlist':
                if values['-PLAYLIST LIST-']:
                    selected_playlist = values['-PLAYLIST LIST-'][0]
                    playlist = self.sys_music.user.playlists[selected_playlist]
                    self.sys_music.audio_player.play_playlist(playlist)
                    window['-QUEUE-'].update(
                        [f"{song.title} - {song.artist} - {song.genre}" for song in
                         self.sys_music.audio_player.queue])
                else:
                    sg.popup('Por favor, selecciona una playlist antes de presionar reproducir playlist')
            elif event == 'Siguiente':
                self.sys_music.audio_player.next()
                window['Pausar'].update('Pausar')
                paused = False
                window['-QUEUE-'].update(
                    [f"{song.title} - {song.artist} - {song.genre}" for song in
                     self.sys_music.audio_player.queue])
            elif event == 'Añadir a la cola':
                if values['-SONG LIST-']:
                    selected_song_details = values['-SONG LIST-'][0].split(' - ')
                    for song in self.sys_music.songs:
                        if [song.title, song.artist, song.genre] == selected_song_details:
                            try:
                                self.sys_music.audio_player.add_to_queue(song)
                                window['-QUEUE-'].update(
                                    [f"{song.title} - {song.artist} - {song.genre}" for song in
                                     self.sys_music.audio_player.queue])
                                break
                            except Exception as e:
                                sg.popup(e)
                else:
                    sg.popup('Por favor, selecciona una canción antes de presionar añadir a la cola')
            elif event == 'Crear playlist aleatoria':
                try:
                    self.sys_music.create_random_playlist()
                    window['-PLAYLIST LIST-'].update(
                        [playlist.name for playlist in self.sys_music.user.playlists.values()])
                except Exception as e:
                    sg.popup(e)
            elif event == 'Recomendar playlist':
                if values['-PLAYLIST LIST-']:
                    try:
                        selected_playlist = values['-PLAYLIST LIST-'][0]
                        recommended_playlist = self.sys_music.recommend_playlist(selected_playlist)
                        self.sys_music.user.playlists[recommended_playlist.name] = recommended_playlist
                        window['-PLAYLIST LIST-'].update(
                            [playlist.name for playlist in self.sys_music.user.playlists.values()])
                    except Exception as e:
                        sg.popup(e)
                else:
                    sg.popup('Por favor, selecciona una playlist antes de presionar recomendar playlist')
            elif event == 'Renombrar playlist':
                if values['-PLAYLIST LIST-']:
                    selected_playlist = values['-PLAYLIST LIST-'][0]
                    self.rename_playlist_gui(selected_playlist)
                    window['-PLAYLIST LIST-'].update(
                        [playlist.name for playlist in self.sys_music.user.playlists.values()])
                else:
                    sg.popup('Por favor, selecciona una playlist antes de presionar renombrar playlist')

        window.close()

    def edit_song_gui(self, song):
        layout = [
            [sg.Text('Title:'), sg.InputText(song.title, key='-TITLE-')],
            [sg.Text('Artist:'), sg.InputText(song.artist, key='-ARTIST-')],
            [sg.Text('Genre:'), sg.InputText(song.genre, key='-GENRE-')],
            [sg.Button('OK'), sg.Button('Cancel')]
        ]
        window = sg.Window('Edit Song', layout)
        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Cancel':
                break
            if event == 'OK':
                song.title = values['-TITLE-']
                song.artist = values['-ARTIST-']
                song.genre = values['-GENRE-']
                break
        window.close()

    def run(self):
        self.start_menu_gui()
