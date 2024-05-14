from sistema_música.model.sis_música import AudioPlayer, SysMusic
from sistema_música.view.sis_música_gui import SysMusicGUI


def main():
    audio_player = AudioPlayer([])
    sys_music_fix = SysMusic(audio_player)
    gui = SysMusicGUI(sys_music_fix)
    gui.run()


if __name__ == "__main__":
    main()
    