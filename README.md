# AUTORES

- Tomás Córdoba Urquijo

# SISTEMA DE MÚSICA

Este proyecto es un reproductor de audio que personaliza la experiencia musical del usuario,
ofreciendo funcionalidades que se adapten a sus gustos y preferencias. Utiliza la biblioteca `pygame` para la reproducción de audio y la biblioteca `threading` para manejar la entrada del usuario en un hilo separado.

## Funcionalidades

- Reproducción de archivos de audio
- Control de volumen
- Pausa, reanudación y detención de la reproducción
- Retroceso de la reproducción
- Cola de reproducción
- Información del usuario
- Creacion de playlist
- Reproducción de playlist
- Generar playlist aleatoria
- Recomendación de canciones

## Cómo usar

1. Inicie el programa en `sistema_musica\sys_music\app.py`. Se le pedirá que ingrese su información de usuario.
2. Se mostrará un menú con las opciones disponibles. Puede ingresar los siguientes comandos:
    - `user info`: Muestra la información del usuario.
    - `add song`: Agrega una canción a la lista de canciones.
    - `songs`: Muestra las canciones disponibles.
    - `play <nombre de la canción>`: Reproduce la canción especificada.
    - `pause`: Pausa la reproducción.
    - `unpause`: Reanuda la reproducción.
    - `stop`: Detiene la reproducción.
    - `rewind`: Retrocede la reproducción.
    - `queue <nombre de la canción>`: Agrega una canción a la cola de reproducción.
    - `next`: Reproduce la siguiente canción en la cola de reproducción.
    - `volume <número>`: Cambia el volumen de la reproducción (entre 0 y 100).
    - `new playlist`: Crea una nueva playlist.
    - `delete playlist`: Elimina una playlist.
    - `rename playlist`: Cambia el nombre de una playlist.
    - `show playlists`: Muestra las playlists disponibles.
    - `add to playlist`: Agrega una canción a una playlist.
    - `remove from playlist`: Elimina una canción de una playlist.
    - `start playlist`: Reproduce una playlist.
    - `random playlist`: Crea una playlist aleatoria.
    - `random song`: Reproduce una canción aleatoria.
    - `recommend playlist`: Crea una playlist recomendada basada en una playlist de referencia.
    - `exit`: Cierra el programa.
  
Puedes encontrar música de prueba en el directorio `sistema_musica\assets`

## Dependencias

Este proyecto depende de las siguientes bibliotecas de Python:

- `pygame`
- `threading`

(Se encuentran en el archivo `requirements.txt`)
