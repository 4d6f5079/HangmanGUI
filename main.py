from game_files_handler import GameFilesHandler
from gui_handler import GUIHandler
from game import Game
from pathlib import Path


def main():
    gui_handler = GUIHandler()
    game_files_handler = GameFilesHandler(
        Path('data (do not modify)/save_file'),
        Path('data (do not modify)/checksum'),
        Path('data (do not modify)/nl_words'),
        gui_handler
    )

    Game(
        gui_handler=gui_handler,
        game_files_handler=game_files_handler
    ).run()


if __name__ == '__main__':
    main()
