from color_enum import RGBColor
from game_files_handler import GameFilesHandler
from gui_handler import GUIHandler
import random
from pygame.event import pump, get
from pygame import QUIT, VIDEORESIZE, KEYDOWN, KEYUP, K_0, K_KP0, K_KP1, K_1
import re
import time


class Game():

    def __init__(
        self,
        gui_handler: GUIHandler,
        game_files_handler: GameFilesHandler
    ) -> None:
        self.game_files_handler = game_files_handler
        self.gui_handler = gui_handler
        self.used_words: set[str] = set()
        self.correctly_guessed_words: int = 0
        self.incorrectly_guessed_words: int = 0
        self.words_list: set[str] = game_files_handler.getting_words()
        self.ask_for_load_save_file_if_present()

    def ask_for_load_save_file_if_present(self):
        res_tup = self.game_files_handler.load_save_file_on_user_answer()
        if res_tup:
            used_words, guessed_words_count, incorrect_guesses_count = res_tup
            self.used_words = used_words
            self.correctly_guessed_words = guessed_words_count
            self.incorrectly_guessed_words = incorrect_guesses_count

    def check_if_all_words_are_used(self):
        if self.used_words == self.words_list:
            self.gui_handler.set_background_color(RGBColor.GREY)

            msg_progress_not_saved = self.gui_handler.show_messagebox_askquestion(
                'ALL WORDS ARE USED',
                'Do you want to DELETE save files?'
            )
            if msg_progress_not_saved == self.gui_handler.QUESTION_ANSWER_YES:
                self.game_files_handler.delete_save_file()
            else:
                self.gui_handler.quit_pygame()

    def get_new_random_word(self):
        # get a random word that has not been used before
        return random.choice(tuple(self.words_list - self.used_words))

    def handle_quit_game(self):
        self.game_files_handler.ask_for_saving_file_handler(
            self.used_words,
            self.correctly_guessed_words,
            self.incorrectly_guessed_words
        )

    def handle_video_resize(self, event, arr_of_the_word, cond):
        width, height = event.dict['size']

        self.gui_handler.resize_window(width, height)

        self.gui_handler.set_background_color(RGBColor.GREY)

        self.gui_handler.show_word(arr_of_the_word)

        self.gui_handler.hangman_states(0)

        for condition in range(cond, 0, -1):
            self.gui_handler.hangman_states(condition)

        self.gui_handler.show_info_and_statistics(
            self.correctly_guessed_words,
            self.incorrectly_guessed_words
        )

    def get_random_unguessed_letter(self, word_letters_lst, used_letters):
        return random.choice(tuple(set(word_letters_lst) - set(used_letters)))

    def run(self):
        """Main loop of the game
        """

        # preventing infinite loop when all words are used
        self.check_if_all_words_are_used()

        # get new unused word from words list
        rand_word = self.get_new_random_word()

        # length of the word
        length_word = len(rand_word)

        # array of the word chosen
        arr_of_the_word = []

        # array for used letters of the chosen word
        used_letters = []

        # fill the list with blank chars
        for _ in range(length_word):
            arr_of_the_word.append("_ ")

        self.gui_handler.show_word(arr_of_the_word)

        # state of hangman character
        cond = 0

        # var to check whether the word has been guessed or the game is over
        word_bool = False

        self.gui_handler.show_info_and_statistics(
            self.correctly_guessed_words,
            self.incorrectly_guessed_words
        )

        try:
            while True:
                pump()

                # draw hang man character
                self.gui_handler.hangman_states(cond)

                for event in get():
                    if event.type == QUIT:
                        self.handle_quit_game()

                    # Make resizing of the game windows possible
                    elif event.type == VIDEORESIZE:
                        self.handle_video_resize(event, arr_of_the_word, cond)

                    elif event.type == KEYDOWN:
                        # exiting the game
                        if event.key == K_0 or event.key == K_KP0:
                            self.game_files_handler.ask_for_saving_file_handler(
                                self.used_words,
                                self.correctly_guessed_words,
                                self.incorrectly_guessed_words
                            )

                        # handling case where user wants a hint
                        elif event.key == K_1 or event.key == K_KP1:

                            # choosing a letter that has not yet been guessed in the word
                            letter_of_hint = self.get_random_unguessed_letter(
                                rand_word, used_letters)

                            # append the letter to the array of the letters of the word
                            for i in range(length_word):
                                if rand_word[i] == letter_of_hint:
                                    arr_of_the_word[i] = letter_of_hint
                                    used_letters.append(letter_of_hint)

                            # make the hinted letter appear
                            self.gui_handler.show_word(arr_of_the_word)

                        # Check whether the guessed letter is present in the word
                        elif re.search("[a-zA-Z]", chr(event.key)):

                            if (
                                (chr(event.key).upper() in rand_word) or
                                (chr(event.key).lower() in rand_word)
                            ) and \
                                (chr(event.key) not in arr_of_the_word
                                 ):
                                for i in range(length_word):
                                    if (rand_word[i] == (chr(event.key)).upper()) or \
                                            (rand_word[i] == (chr(event.key)).lower()):
                                        arr_of_the_word[i] = rand_word[i]

                            else:
                                # check whether the letter has already been used, if not then store it in used words array and count
                                # it as wrong letter
                                if (chr(event.key) in used_letters) or (chr(event.key) in arr_of_the_word):
                                    self.gui_handler.display_text_and_blit(
                                        "ALREADY USED LETTER " +
                                        chr(event.key).upper(),
                                        self.gui_handler.fonts_dict.get(
                                            'FreeSansBold25'),
                                        RGBColor.RED.value,
                                        500,
                                        100
                                    )
                                else:
                                    # if ticked letter is not in the word and not used before
                                    used_letters.append(chr(event.key))
                                    cond = cond + 1

                            self.gui_handler.show_word(arr_of_the_word)

                            # to make some time to draw line
                            time.sleep(0.05)

                        else:
                            self.gui_handler.display_text_and_blit(
                                "INVALID INPUT!",
                                self.gui_handler.fonts_dict.get(
                                    'FreeSansBold33'),
                                RGBColor.RED.value,
                                500,
                                100
                            )

                    # hide invalid input msg after it appears
                    elif event.type == KEYUP:
                        self.gui_handler.draw_rect(
                            RGBColor.GREY, (260, 50, 500, 100))

                # handling case where the user wasn't able to guess the word
                if cond == 10:
                    self.gui_handler.render_incorrect_guess_word(
                        cond, rand_word)

                    self.incorrectly_guessed_words += 1

                    word_bool = True

                # handling case where the user was able to guess the word
                elif "".join(arr_of_the_word) == rand_word:
                    self.gui_handler.render_correct_guess_word(rand_word)

                    self.correctly_guessed_words += 1

                    word_bool = True

                self.gui_handler.update_pygame_screen()

                if word_bool is True:
                    # append the new word so that it doesn't get used anymore
                    self.used_words.add(rand_word)

                    time.sleep(1)
                    self.gui_handler.set_background_color(RGBColor.GREY)
                    self.run()

        except Exception as e:
            print(e)
