from src.model.music_system_algorithm import AudioPlayer, SysMusic
from src.view.music_system_GUI import SysMusicGUI


def main():
    audio_player = AudioPlayer([])
    sys_music_fix = SysMusic(audio_player)
    gui = SysMusicGUI(sys_music_fix)
    gui.run()


if __name__ == "__main__":
    main()
    