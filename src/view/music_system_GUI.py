import PySimpleGUI as sg
from pathlib import Path
from src.model.music_system_algorithm import Song, User, SysMusic
from src.exceptions.exceptions import (InvalidNameError, InvalidEmailError)


class SysMusicGUI:
    sg.theme('DarkAmber')

    def __init__(self, sys_music: SysMusic):
        self.sys_music = sys_music

    def start_menu_gui(self):
        layout = [
            [sg.Text('Sistema de música', font=('Book', 20))],
            [sg.Text('')],
            [sg.Image(str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'music_icon.png')),
                      subsample=4)],
            [sg.Text('')],
            [sg.Text('¡Bienvenido al sistema de música!')],
            [sg.Text('')],
            [sg.Button('Iniciar', size=(8, 2), border_width=0), sg.Button('Salir', size=(8, 2), border_width=0)]
        ]

        window = sg.Window('Sistema de música', layout, element_justification='c', finalize=True, margins=(10, 10),
                           resizable=True)

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
                [sg.Text('Ingrese su nombre:'), sg.InputText(key='-NAME-', expand_x=True, size=(20, 1))],
                [sg.Text('Ingrese su email:'), sg.InputText(key='-EMAIL-', expand_x=True, size=(20, 1))],
                [sg.Button('Ok', border_width=0, size=(8, 1))]
            ]

            window = sg.Window('Información del usuario', layout, element_justification='c', resizable=True,
                               margins=(10, 10))

            while True:
                event, values = window.read()
                if event == sg.WINDOW_CLOSED:
                    exit()
                elif event == 'Ok':
                    name = values['-NAME-']
                    email = values['-EMAIL-']
                    try:
                        if not name.isalpha():
                            raise InvalidNameError("El nombre solo puede contener letras")
                        if "@" not in email or "." not in email:
                            raise InvalidEmailError("El email debe contener @ y .")
                        self.sys_music.user = User(name, email)
                        window.close()
                        return
                    except (InvalidNameError, InvalidEmailError) as e:
                        sg.popup(str(e))
                        break

            window.close()

    def show_user_info_gui(self):
        info = [
            [sg.Text('Nombre:')],
            [sg.Text('Email:')],
        ]

        inputs = [
            [sg.Text(self.sys_music.user.name)],
            [sg.Text(self.sys_music.user.email)]
        ]

        user_info = [
            [sg.Column(info, element_justification='l'), sg.Column(inputs, element_justification='l')]
        ]

        layout = [
            [sg.Frame('Información del usuario', layout=user_info, element_justification='c', expand_x=True)],
            [sg.Button('Ok', border_width=0)]
        ]

        window = sg.Window('', layout, element_justification='c', resizable=True, margins=(10, 10))

        while True:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED or event == 'Ok':
                break

        window.close()

    def add_song_gui(self, file_path: str):
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

    def edit_song_gui(self, song: Song):
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
                try:
                    self.sys_music.change_song_title(song, values['-TITLE-'])
                    self.sys_music.change_song_artist(song, values['-ARTIST-'])
                    self.sys_music.change_song_genre(song, values['-GENRE-'])
                except Exception as e:
                    sg.popup(e)
                break

        window.close()

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

    def rename_playlist_gui(self, playlist_name: str):
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

    def open_playlist_gui(self, playlist_name: str):
        playlist = self.sys_music.user.playlists[playlist_name]
        song_list = [f"{song.title} - {song.artist} - {song.genre}" for song in playlist.songs]

        playlist_songs = [
            [sg.Listbox(values=song_list, size=(50, 10), key='-SONG LIST-', expand_y=True, expand_x=True)],
        ]

        songs_list = [
            [sg.Listbox(values=[f"{song.title} - {song.artist} - {song.genre}" for song in self.sys_music.songs],
                        size=(50, 10), key='-SONG LIST AVAILABLE-', expand_y=True, expand_x=True)],
        ]

        buttons = [
            [sg.Button(key='Añadir canción', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'add.png')),
                       image_subsample=30, button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Button(key='Eliminar canción', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'delete.png')),
                       image_subsample=30, button_color=(sg.theme_background_color(), sg.theme_background_color()))],
        ]

        layout = [
            [sg.Frame('Canciones en la playlist', layout=playlist_songs, element_justification='c', expand_y=True)],
            [sg.Frame('', layout=buttons, element_justification='c')],
            [sg.Frame('Canciones disponibles', layout=songs_list, element_justification='c', expand_y=True)],
            [sg.Button('OK', border_width=0)]
        ]

        window = sg.Window('Ver playlist', layout, resizable=True, element_justification='c', finalize=True)

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

    def create_music_player_gui(self):
        try:
            user_name = self.sys_music.user.name
        except AttributeError:
            sg.popup('Por favor, ingrese su información de usuario antes de continuar')
            return

        header = [
            [sg.Button(key='-USER INFO-', tooltip='Información del usuario', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'user.png')),
                       image_subsample=25, use_ttk_buttons=True,
                       button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Text(f'¡Hola, {user_name}!')]
        ]

        col_playlist = [
            [sg.Text('Playlists del usuario:')],
            [sg.Listbox(values=[], size=(50, 2), key='-PLAYLIST LIST-', bind_return_key=True, expand_y=True,
                        justification='left')],
            [sg.Button(key='-PLAY PLAYLIST-', tooltip='Reproducir playlist', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'play.png')),
                       image_subsample=30, button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Button(key='-CREATE PLAYLIST-', tooltip='Crear playlist', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'add.png')),
                       image_subsample=30, button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Button(key='-DELETE PLAYLIST-', tooltip='Eliminar playlist', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'delete.png')),
                       image_subsample=30, button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Button('Abrir', tooltip='Abrir y editar playlist seleccionada', border_width=0),
             sg.Button('Renombrar', tooltip='Renombrar playlist seleccionada', border_width=0), ]

        ]

        col_songs = [
            [sg.Text('Canciones disponibles:')],
            [sg.Listbox(values=[], size=(50, 2), key='-SONG LIST-', bind_return_key=True, expand_y=True,
                        justification='center', right_click_menu=['', ['Agregar canciones']])],
            [sg.Button(key='-EDIT SONG-', tooltip='Editar información de canción', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'edit.png')),
                       image_subsample=30, button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Button(key='-DELETE SONG-', tooltip='Eliminar canción', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'X.png')),
                       image_subsample=30, button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Button(key='-ADD TO QUEUE-', tooltip='Añadir a la cola', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'queue.png')),
                       image_subsample=30, button_color=(sg.theme_background_color(), sg.theme_background_color())), ]
        ]

        col_queue = [
            [sg.Text('Canciones en la cola:')],
            [sg.Listbox(values=[], size=(50, 2), key='-QUEUE-', bind_return_key=True, expand_y=True,
                        justification='right')],
            [sg.Button('Quitar de la cola', tooltip='Eliminar de la cola la canción seleccionada', border_width=0), ]
        ]

        generate_playlists = [
            [sg.Button('Recomendar playlist',
                       tooltip='Recomienda una playlist con generos similares a la playlist seleccionada',
                       border_width=0),
             sg.Button('Crear playlist aleatoria', tooltip='Crea una playlist aleatoria', border_width=0)]
        ]

        lists = [
            [sg.Frame('', layout=col_playlist, element_justification='l', expand_y=True, border_width=0),
             sg.Frame('', layout=col_songs, element_justification='c', expand_y=True, border_width=0),
             sg.Frame('', layout=col_queue, element_justification='r', expand_y=True, border_width=0)],
        ]

        col_volume = [
            [sg.Image(source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'volume.png')),
                      subsample=25),
             sg.Slider(range=(0, 100), orientation='horizontal', size=(20, 10),
                       key='-VOLUME SLIDER-', default_value=50)],
        ]

        buttons = [
            [sg.Button(key='-PLAY MUSIC-', tooltip='Reproduce la canción seleccionada', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'play.png')),
                       image_subsample=25, button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Button(key='-PAUSE MUSIC-', tooltip='Pausa la canción seleccionada', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'pause.png')),
                       image_subsample=25, button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Button(key='-STOP MUSIC-', tooltip='Para la canción seleccionada', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'stop.png')),
                       image_subsample=25, button_color=(sg.theme_background_color(), sg.theme_background_color())),
             sg.Button(key='-NEXT SONG-', tooltip='Pasa a la siguiente canción', border_width=0,
                       image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'next.png')),
                       image_subsample=25, button_color=(sg.theme_background_color(), sg.theme_background_color())), ]
        ]

        player = [
            [sg.Frame('', layout=buttons, element_justification='c', expand_y=True, border_width=0),
             sg.Text('                    '),
             sg.Frame('', layout=col_volume, element_justification='l', expand_y=True, border_width=0)]
        ]

        file_browser = [
            [sg.Input(key='-FILE-', visible=False, enable_events=True),
             sg.FileBrowse(file_types=(("MP3 Files", "*.mp3"),), button_text='Agregar canción al sistema',
                           tooltip='Agrega un archivo de música al sistema')],
        ]

        layout = [
            [sg.Frame('', layout=header, element_justification='c', expand_x=True)],
            [sg.Frame('', layout=file_browser, element_justification='c', expand_x=True)],
            [sg.Frame('', layout=lists, element_justification='c', expand_x=True, expand_y=True)],
            [sg.Frame('Generar playlists', layout=generate_playlists, element_justification='c', expand_x=True)],
            [sg.Frame('', layout=player, element_justification='c', expand_x=True)]
        ]

        return layout

    def update_pause_button(self, window: sg.Window):
        window['-PAUSE MUSIC-'].update(
            image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'pause.png')),
            image_subsample=25
        )

    def update_resume_button(self, window: sg.Window):
        window['-PAUSE MUSIC-'].update(
            image_source=str((Path(__file__).resolve().parents[2] / 'assets' / 'Icons' / 'resume.png')),
            image_subsample=25
        )

    def music_player_gui(self):
        layout = self.create_music_player_gui()

        window = sg.Window('Sistema de música', layout, finalize=True, resizable=True)

        window['-SONG LIST-'].update(
            [f"{song.title} - {song.artist} - {song.genre}" for song in self.sys_music.songs])

        paused = False

        while True:
            event, values = window.read(timeout=100)

            if event == sg.WINDOW_CLOSED:
                break

            elif event == sg.TIMEOUT_EVENT:
                self.sys_music.audio_player.set_volume(int(values['-VOLUME SLIDER-']) / 100)
                if not self.sys_music.audio_player.is_music_playing():
                    if not paused:
                        self.sys_music.audio_player.next()
                        window['-QUEUE-'].update(
                            [f"{song.title} - {song.artist} - {song.genre}" for song in
                             self.sys_music.audio_player.queue])

            elif event == '-FILE-':
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

            elif event == '-DELETE SONG-':
                if values['-SONG LIST-']:
                    self.sys_music.audio_player.stop()
                    self.update_pause_button(window)
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

            elif event == '-USER INFO-':
                self.show_user_info_gui()

            elif event == '-PLAY MUSIC-':
                if values['-SONG LIST-']:
                    self.update_pause_button(window)
                    paused = False
                    selected_song_details = values['-SONG LIST-'][0].split(' - ')
                    for song in self.sys_music.songs:
                        if [song.title, song.artist, song.genre] == selected_song_details:
                            self.sys_music.audio_player.play(song)
                            break
                else:
                    sg.popup('Por favor, selecciona una canción antes de presionar reproducir')

            elif event == '-PAUSE MUSIC-':
                if self.sys_music.audio_player.is_playing:
                    if paused:
                        self.sys_music.audio_player.unpause()
                        self.update_pause_button(window)
                        paused = False
                    else:
                        self.sys_music.audio_player.pause()
                        self.update_resume_button(window)
                        paused = True
                else:
                    sg.popup('No hay canciones para pausar')

            elif event == '-STOP MUSIC-':
                if self.sys_music.audio_player.is_playing:
                    self.update_pause_button(window)
                    paused = False
                    self.sys_music.audio_player.stop()
                else:
                    sg.popup('No hay canciones para parar')

            elif event == '-NEXT SONG-':
                self.sys_music.audio_player.next()
                self.update_pause_button(window)
                paused = False
                window['-QUEUE-'].update(
                    [f"{song.title} - {song.artist} - {song.genre}" for song in
                     self.sys_music.audio_player.queue])

            elif event == '-EDIT SONG-':
                if values['-SONG LIST-']:
                    self.sys_music.audio_player.stop()
                    self.update_pause_button(window)
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

            elif event == '-ADD TO QUEUE-':
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

            elif event == 'Quitar de la cola':
                if values['-QUEUE-']:
                    selected_song_details = values['-QUEUE-'][0].split(' - ')
                    for song in self.sys_music.songs:
                        if [song.title, song.artist, song.genre] == selected_song_details:
                            try:
                                self.sys_music.audio_player.remove_from_queue(song)
                                window['-QUEUE-'].update(
                                    [f"{song.title} - {song.artist} - {song.genre}" for song in
                                     self.sys_music.audio_player.queue])
                                break
                            except Exception as e:
                                sg.popup(e)
                else:
                    sg.popup('Por favor, selecciona una canción antes de presionar añadir a la cola')

            elif event == '-CREATE PLAYLIST-':
                self.create_playlist_gui()
                window['-PLAYLIST LIST-'].update(
                    [playlist.name for playlist in self.sys_music.user.playlists.values()])

            elif event == '-DELETE PLAYLIST-':
                if values['-PLAYLIST LIST-']:
                    selected_playlist = values['-PLAYLIST LIST-'][0]
                    self.sys_music.user.delete_playlist(selected_playlist)
                    window['-PLAYLIST LIST-'].update(
                        [playlist.name for playlist in self.sys_music.user.playlists.values()])
                else:
                    sg.popup('Por favor, selecciona una playlist antes de presionar eliminar')

            elif event == 'Abrir':
                if values['-PLAYLIST LIST-']:
                    selected_playlist = values['-PLAYLIST LIST-'][0]
                    self.open_playlist_gui(selected_playlist)
                else:
                    sg.popup('Por favor, selecciona una playlist antes de presionar Ver playlist')

            elif event == 'Renombrar':
                if values['-PLAYLIST LIST-']:
                    selected_playlist = values['-PLAYLIST LIST-'][0]
                    self.rename_playlist_gui(selected_playlist)
                    window['-PLAYLIST LIST-'].update(
                        [playlist.name for playlist in self.sys_music.user.playlists.values()])
                else:
                    sg.popup('Por favor, selecciona una playlist antes de presionar renombrar playlist')

            elif event == '-PLAY PLAYLIST-':
                if values['-PLAYLIST LIST-']:
                    selected_playlist = values['-PLAYLIST LIST-'][0]
                    playlist = self.sys_music.user.playlists[selected_playlist]
                    self.sys_music.audio_player.play_playlist(playlist)
                    window['-QUEUE-'].update(
                        [f"{song.title} - {song.artist} - {song.genre}" for song in
                         self.sys_music.audio_player.queue])
                else:
                    sg.popup('Por favor, selecciona una playlist antes de presionar reproducir playlist')

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

        window.close()

    def run(self):
        self.start_menu_gui()
