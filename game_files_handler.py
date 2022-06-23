import hashlib
from tkinter import *
from tkinter import messagebox
import pygame
import os
from pathlib import Path
from gui_handler import GUIHandler


class GameFilesHandler():

    def __init__(
        self,
        save_file_path: Path,
        checksum_file_path: Path,
        words_file_name: Path,
        gui_handler: GUIHandler,
        buffer_size=65536
    ) -> None:
        """Constructor for GameFilesHanlder

        Args:
            save_file_path (Path): The path to the save file
            checksum_file_path (Path): The path to the checksum file
            words_file_name (Path): Path to the file containing the words
            gui_handler (GUIHandler): Handles GUI graphics
            buffer_size (int, optional): Chunks to read at time. Defaults to 65536 (64kb).
        """
        self.save_file_path = save_file_path
        self.checksum_file_path = checksum_file_path
        self.words_file_name = words_file_name
        self.gui_handler = gui_handler
        self.buffer_size = buffer_size

    def sha256_hash_digest(self, file_name_to_hash=None):
        """Calculates sha256 hash for checking the integrity of the given file

        Args:
            file_name_to_hash (Path): Path to the file from which to calculates the hash. Default is save file path.

        Returns:
            str: The hash digest of the file
        """

        if not file_name_to_hash:
            file_name_to_hash = self.save_file_path

        # the sha256 hash to use for digest
        sha256_hash = hashlib.sha256()

        with open(file_name_to_hash, 'rb') as sf:
            while True:
                data = sf.read(self.buffer_size)
                if not data:
                    break
                sha256_hash.update(data)

        return sha256_hash.hexdigest()

    def sha256_hash_check(self, file_to_check, checksum):
        """Checks whether the file to check is not tampered with using calculated checksum

        Args:
            file_to_check (Path): The path to the file that should be checked
            checksum (str): The sha256 hash to check with the hash of the file_to_check

        Returns:
            bool: True if the file has the same hash as checksum. False otherwise.
        """
        hash_digested = self.sha256_hash_digest(file_to_check)

        if checksum == hash_digested:
            return True
        else:
            return False

    def saving_progress(
        self,
        used_words_set,
        correctly_guessed_words,
        incorrectly_guessed_words
    ):
        """Saves seen words and correctly/incorrectly guessed words count in the save file

        Args:
            used_words_arr (set): Set containing the words used/seen
            correctly_guessed_words (int): Count of how many words are correctly guessed
            incorrectly_guessed_words (int): Count of how many words are incorrectly guessed
        """
        try:
            with open(self.save_file_path, "w") as f:

                f.write(','.join(used_words_set) + '\n')
                f.write(str(correctly_guessed_words) + '\n')
                f.write(str(incorrectly_guessed_words))
                print("saved progress successfully!")

            with open(self.checksum_file_path, "w") as checksum_file:
                checksum_file.write(
                    self.sha256_hash_digest(self.save_file_path))

        except ValueError:
            self.gui_handler.show_messagebox_error(
                'CAN\'T CREATE SAVE FILE',
                'Please notify the creator of this game to solve this problem.'
            )
            self.gui_handler.quit_pygame()

    def ask_for_saving_file_handler(
            self,
            used_words_set,
            correctly_guessed_words,
            incorrectly_guessed_words
    ):
        yes_rect, no_rect = self.gui_handler.render_save_to_file_scene()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    answer = self.gui_handler.show_messagebox_askquestion(
                        'WARNING: PROGRESS NOT SAVED!',
                        'Your progress isn\'t saved. Do you really want '
                        'to quit without saving progress?'
                    )
                    if answer == self.gui_handler.QUESTION_ANSWER_YES:
                        self.gui_handler.quit_pygame()

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()

                    if yes_rect.collidepoint(mouse_pos):
                        self.saving_progress(
                            used_words_set,
                            correctly_guessed_words,
                            incorrectly_guessed_words
                        )

                        self.gui_handler.render_yes_rect_clicked_scene()

                        self.gui_handler.quit_pygame()

                    if no_rect.collidepoint(mouse_pos):
                        answer = self.gui_handler.show_messagebox_askquestion(
                            'WARNING!!!',
                            'You are about to exit the game without saving! '
                            'Are you sure you DON\'T want to save your progress?'
                        )
                        if answer == self.gui_handler.QUESTION_ANSWER_YES:
                            self.gui_handler.quit_pygame()

    def delete_save_file(self):
        if Path.exists(self.save_file_path) and Path.exists(self.checksum_file_path):
            os.remove(self.save_file_path)
            os.remove(self.checksum_file_path)
            self.gui_handler.show_messagebox_info(
                'SAVE FILES DELETED',
                'Save files deleted successfully.'
            )
        else:
            self.gui_handler.show_messagebox_error(
                'CAN\'T DELETE SAVE FILE',
                'There are no save files to be deleted.'
            )

        pygame.quit()
        quit()

    # if save file exists in root folder, set guessed_words, incorrect_guesses and
    # used_words to those values. If no save file exists then set everything to default values
    def load_save_file(self):
        """Loads the data from the save file after validating the integrity of the save file

        Returns:
            tuple(set, int, int): (used_words, guessed_words_count, incorrect_guesses_count)
        """
        try:
            used_words = set()
            guessed_words_count = -1
            incorrect_guesses_count = -1

            with open(self.save_file_path, 'r') as file:
                with open(self.checksum_file_path, 'r') as get_checksum:
                    the_checksum = get_checksum.readline()

                    if self.sha256_hash_check(self.save_file_path, the_checksum):
                        pass
                    else:
                        self.gui_handler.show_messagebox_error(
                            'HASH UNMATCH FOUND',
                            'Save File has been tempered with! Exiting Game ...'
                        )
                        self.gui_handler.quit_pygame()

                first_line = file.readline()

                # checking whether the first line is empty (this causes reading issues)
                # thus checking for it is necessary for stable file reading
                if first_line == "\n":
                    pass
                else:
                    used_words = {x.strip() for x in first_line.split(',')}

                guessed_words_count = int(
                    file.readline().replace("\n", "").replace(",", "")
                )
                incorrect_guesses_count = int(file.readline())

                return used_words, guessed_words_count, incorrect_guesses_count

        except FileNotFoundError:
            self.gui_handler.show_messagebox_error(
                'NO SAVE FILES FOUND',
                'No save files found called \'save_file\'. '
                'All game variables are set to default values. '
                'Please click \'ok\' to continue to the game. '
            )

        except ValueError:
            self.gui_handler.show_messagebox_error(
                'CAN\'T READ SAVE FILE',
                'Please remove all changes done to save file and checksum '
                'file, check whether the file extension of both checksum and save file are ".file"'
                ' or delete the save file to be able to start the game'
            )
            self.gui_handler.quit_pygame()

        return None

    def load_save_file_on_user_answer(self):
        if self.save_file_path.is_file():
            answer = self.gui_handler.show_messagebox_askquestion(
                'LOAD SAVE FILE?',
                'Do you want to load your save file?'
            )
            if answer == self.gui_handler.QUESTION_ANSWER_YES:
                loaded_save_file_tup = self.load_save_file()
                if loaded_save_file_tup:
                    self.gui_handler.show_messagebox_info(
                        'CONFIRMATION MESSAGE',
                        'SAVE FILE LOADED SUCCESSFULLY!'
                    )
                    return loaded_save_file_tup
                else:
                    self.gui_handler.show_messagebox_info(
                        'ERROR MESSAGE',
                        'SOMETHING UNEXPECTED HAPPENED WHILE LOADING THE SAVE FILE!'
                        'PLEASE NOTIFY ADMIN ABOUT THIS ERROR.'
                    )
                    self.gui_handler.quit_pygame()
        return None

    def getting_words(self):
        """Opening the file once and read the words from it and return it

        ### replaced try/except snippet from main() to here
        ### so that the file gets opened once and not every time main() gets called
        ### (this of course for efficiency)

        Returns:
            set[str]: Set of words as strings
        """
        try:
            with open(self.words_file_name, "r") as words_file:
                return set(words_file.read().splitlines())
        except IOError:
            self.gui_handler.show_messagebox_error(
                'WORDSLIST NOT FOUND!',
                'Words list of the game is missing! Try to re-download the wordslist '
                'from the download link of the game.'
            )
            self.gui_handler.quit_pygame()
