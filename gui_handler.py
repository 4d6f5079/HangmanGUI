from ctypes.wintypes import RGB
import pygame
from color_enum import RGBColor
from pygame.locals import RESIZABLE
from tkinter import *
from tkinter import messagebox
import time
from pygame.display import set_mode


class GUIHandler():

    QUESTION_ANSWER_YES = 'yes'
    QUESTION_ANSWER_NO = 'no'

    def __init__(
        self,
    ) -> None:
        self.screen_size_info = self.setup_pygame()
        self.fonts_dict = self.init_fonts_dict()
        self.game_display = self.init_game_window()

    def setup_pygame(self):
        # Init the pygame modules and save info about screen size info
        pygame.init()

        # Name the game window
        pygame.display.set_caption('Hangman Game')

        return pygame.display.Info()

    def init_fonts_dict(self):
        return {
            'FreeSansBold33': pygame.font.Font("freesansbold.ttf", 33),
            'FreeSansBold25': pygame.font.Font("freesansbold.ttf", 25),
            'FreeSansBold17': pygame.font.Font("freesansbold.ttf", 17),
            'FreeSansBold16': pygame.font.Font("freesansbold.ttf", 16),
        }

    def init_game_window(
        self,
        width: int = 795,
        height: int = 450,
        background_color: tuple = RGBColor.GREY.value
    ):
        # Setting width and height of the GUI (params have to be tuples so NOT list or separate numbers
        # inputted in the setmode func.
        gameDisplay = pygame.display.set_mode((width, height), RESIZABLE)
        gameDisplay.fill(background_color)
        pygame.display.update()
        return gameDisplay

    def show_info_and_statistics(self, guessed_words, incorrect_guesses):
        """Shows the correctly/incorrectly guessed words on the game window

        Args:
            guessed_words (int): Correctly guessed words
            incorrect_guesses (int): Incorrectly guessed words
        """
        self.game_display.blit(self.fonts_dict.get('FreeSansBold17')
                               .render("Press 0 to quit game and 1 for a hint", True, RGBColor.BLACK.value), (20, 10))

        self.game_display.blit(self.fonts_dict.get('FreeSansBold16')
                               .render("Correctly guessed words: " + str(guessed_words), True, RGBColor.BLACK.value), (550, 10))

        self.game_display.blit(self.fonts_dict.get('FreeSansBold16')
                               .render("Incorrect guesses: " + str(incorrect_guesses), True, RGBColor.BLACK.value), (607, 27))

    def show_word(self, word_array):
        # draw white rect to prevent chaos of multiple layers above each other of the word
        # this is needed for smooth transitions of ASCII
        pygame.draw.rect(self.game_display,
                         RGBColor.GREY.value, (240, 210, 550, 80))

        self.display_text_and_blit(
            " ".join(word_array),
            self.fonts_dict.get('FreeSansBold33'),
            RGBColor.BLACK.value,
            523,
            250
        )

    def draw_rect(self, color: "RGBColor", position: "tuple"):
        return pygame.draw.rect(self.game_display, color.value, position)

    def display_text_and_blit(self, text, font, color, x, y):
        """Displays text on game window given font, color, x and y of the text
        Creates text and centers its rectangle at (x, y) 

        Args:
            text (str): The text to show
            font (pygame.Font): Type of font to use to show the text in
            color (RGBColor): Type of color of the text
            x (int): X coordinate of the text placement
            y (int): Y coordinate of the text placement
        """
        text_msg = font.render(text, True, color)
        text_msg_rect = text_msg.get_rect()
        text_msg_rect.center = (x, y)
        self.game_display.blit(text_msg, text_msg_rect)

    def render_save_to_file_scene(self):
        self.set_background_color(RGBColor.GREY)

        self.display_text_and_blit(
            "SAVE PROGRESS?",
            self.fonts_dict.get('FreeSansBold25'),
            RGBColor.RED.value,
            387,
            190
        )

        # rect for YES
        yes_rect = self.draw_rect(RGBColor.BLUE, (220, 245, 75, 55))
        self.game_display.blit(self.fonts_dict.get('FreeSansBold25')
                               .render('YES', True, (255, 0, 0)), (230, 260))

        # rect for NO
        no_rect = self.draw_rect(RGBColor.BLUE, (457, 245, 75, 55))
        self.game_display.blit(self.fonts_dict.get(
            'FreeSansBold25').render('NO', True, (255, 0, 0)), (474, 260))

        pygame.display.update()

        return yes_rect, no_rect

    def render_yes_rect_clicked_scene(self):
        self.game_display.fill(RGBColor.GREY.value)

        self.display_text_and_blit(
            "PROGRESS SAVED SUCCESSFULLY!",
            self.fonts_dict.get('FreeSansBold25'),
            RGBColor.RED.value,
            387,
            190
        )

        pygame.display.update()
        time.sleep(0.5)

        self.display_text_and_blit(
            "EXITING GAME ...",
            self.fonts_dict.get('FreeSansBold25'),
            RGBColor.BLACK.value,
            387,
            230
        )

        pygame.display.update()
        time.sleep(0.25)

    def show_messagebox_askquestion(self, msg_header, msg_body):
        Tk().wm_withdraw()  # to hide the main window
        msg_progress = messagebox.askquestion(
            msg_header,
            msg_body,
            icon='warning'
        )
        return msg_progress

    def show_messagebox_info(self, msg_header, msg_body):
        Tk().wm_withdraw()
        messagebox.showinfo(
            msg_header,
            msg_body
        )

    def quit_pygame(self):
        pygame.quit()
        quit()

    def show_messagebox_error(self, msg_header, msg_body):
        Tk().wm_withdraw()  # to hide the main window
        messagebox.showerror(msg_header, msg_body)

    def get_game_display(self):
        return self.game_display

    def set_background_color(self, color: RGBColor):
        self.game_display.fill(color.value)

    def get_screensize_info(self):
        return self.screen_size_info

    def resize_window(self, new_width, new_height):
        if (new_width, new_height) == (self.screen_size_info.current_w, self.screen_size_info.current_h):
            new_width = 795
            new_height = 450

        # print(width, " ", height)
        # print("FULLSCREEN: ", pygame.FULLSCREEN)

        # limiting resizing width and height
        if new_width < 775 or new_width > 830:
            new_width = 795

        if new_height != 450:
            new_height = 450

        set_mode((new_width, new_height), RESIZABLE)

    def update_pygame_screen(self):
        pygame.display.update()
        pygame.time.Clock().tick(60)  # 30fps

    def render_incorrect_guess_word(self, cond, word):
        self.set_background_color(RGBColor.GREY)

        self.hangman_states(cond + 1)

        self.display_text_and_blit(
            "YOU LOST!",
            self.fonts_dict.get('FreeSansBold33'),
            RGBColor.RED.value,
            450,
            250
        )

        self.display_text_and_blit(
            "The words is:",
            self.fonts_dict.get('FreeSansBold33'),
            RGBColor.GREEN.value,
            450,
            285
        )

        self.display_text_and_blit(
            word,
            self.fonts_dict.get('FreeSansBold33'),
            RGBColor.BLACK.value,
            450,
            318
        )

    def render_correct_guess_word(self, word):
        self.set_background_color(RGBColor.GREY)

        self.display_text_and_blit(
            "YOU GUESSED THE RIGHT WORD!",
            self.fonts_dict.get('FreeSansBold33'),
            RGBColor.GREEN.value,
            400,
            220
        )

        self.display_text_and_blit(
            "The word is:",
            self.fonts_dict.get('FreeSansBold33'),
            RGBColor.GREEN.value,
            400,
            250
        )

        self.display_text_and_blit(
            word,
            self.fonts_dict.get('FreeSansBold33'),
            RGBColor.BLACK.value,
            400,
            285
        )

    def hangman_states(self, condition):
        """Function responsible for drawing the parts for hangman given a condition

        Args:
            condition (int): Condition/State number of hangman
        """
        if condition == 0:
            pygame.draw.line(self.game_display, RGBColor.BLACK.value,
                             (10, 400), (300, 400), 8)  # baseline
            pygame.draw.line(self.game_display, RGBColor.BLACK.value,
                             (50, 50), (50, 400), 8)  # stick1
            pygame.draw.line(self.game_display, RGBColor.BLACK.value,
                             (50, 60), (250, 60), 8)  # stick2
            pygame.draw.line(self.game_display, RGBColor.BLACK.value,
                             (150, 60), (150, 100), 8)  # rope
            pygame.draw.circle(self.game_display,
                               RGBColor.BLACK.value, (150, 150), 50, 8)  # head
            pygame.draw.line(self.game_display, RGBColor.BLACK.value,
                             (150, 200), (150, 300), 8)  # body
            pygame.draw.line(self.game_display, RGBColor.BLACK.value,
                             (150, 210), (100, 250), 8)  # lefthand
            pygame.draw.line(self.game_display, RGBColor.BLACK.value,
                             (150, 210), (200, 250), 8)  # righthand
            pygame.draw.line(self.game_display, RGBColor.BLACK.value,
                             (150, 300), (100, 350), 8)  # leftleg
            pygame.draw.line(self.game_display, RGBColor.BLACK.value,
                             (150, 300), (200, 350), 8)  # rightleg

        elif condition == 1:
            pygame.draw.line(self.game_display, RGBColor.RED.value,
                             (10, 400), (300, 400), 8)  # baseline

        elif condition == 2:
            pygame.draw.line(self.game_display, RGBColor.RED.value,
                             (50, 50), (50, 400), 8)  # stick1

        elif condition == 3:
            pygame.draw.line(self.game_display, RGBColor.RED.value,
                             (50, 60), (250, 60), 8)  # stick2

        elif condition == 4:
            pygame.draw.line(self.game_display, RGBColor.RED.value,
                             (150, 60), (150, 100), 8)  # rope

        elif condition == 5:
            pygame.draw.circle(self.game_display,
                               RGBColor.RED.value, (150, 150), 50, 8)  # head

        elif condition == 6:
            pygame.draw.line(self.game_display, RGBColor.RED.value,
                             (150, 200), (150, 300), 8)  # body

        elif condition == 7:
            pygame.draw.line(self.game_display, RGBColor.RED.value,
                             (150, 210), (100, 250), 8)  # lefthand

        elif condition == 8:
            pygame.draw.line(self.game_display, RGBColor.RED.value,
                             (150, 210), (200, 250), 8)  # righthand

        elif condition == 9:
            pygame.draw.line(self.game_display, RGBColor.RED.value,
                             (150, 300), (100, 350), 8)  # leftleg

        elif condition == 10:
            pygame.draw.line(self.game_display, RGBColor.RED.value,
                             (150, 300), (200, 350), 8)  # rightleg

        # At this point the game is over
        elif condition == 11:
            pygame.draw.line(self.game_display, RGBColor.BLUE.value,
                             (10, 400), (300, 400), 8)  # baseline
            pygame.draw.line(self.game_display, RGBColor.BLUE.value,
                             (50, 50), (50, 400), 8)  # stick1
            pygame.draw.line(self.game_display, RGBColor.BLUE.value,
                             (50, 60), (250, 60), 8)  # stick2
            pygame.draw.line(self.game_display, RGBColor.BLUE.value,
                             (150, 60), (150, 100), 8)  # rope
            pygame.draw.circle(self.game_display,
                               RGBColor.BLUE.value, (150, 150), 50, 8)  # head
            pygame.draw.line(self.game_display, RGBColor.BLUE.value,
                             (150, 200), (150, 300), 8)  # body
            pygame.draw.line(self.game_display, RGBColor.BLUE.value,
                             (150, 210), (100, 250), 8)  # lefthand
            pygame.draw.line(self.game_display, RGBColor.BLUE.value,
                             (150, 210), (200, 250), 8)  # righthand
            pygame.draw.line(self.game_display, RGBColor.BLUE.value,
                             (150, 300), (100, 350), 8)  # leftleg
            pygame.draw.line(self.game_display, RGBColor.BLUE.value,
                             (150, 300), (200, 350), 8)  # rightleg
