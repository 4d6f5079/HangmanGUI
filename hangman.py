import random
import pygame
import time
from tkinter import *
from tkinter import messagebox
from pygame.locals import RESIZABLE
import os
from color_enum import RGBColor

'''
TODO: 

1 - MAKE SAVING OF PROGRESS OPTION POSSIBLE WHEN USER QUITS THE GAME. 
    (write used_words array contents, correct guesses and incorrect guesses amounts in a CSV file
    , and fetch everything from that file ONLY WHEN such file exists in root folder instead of starting from the beginning) ----> DONE

2 - ADD POSSIBILITY FOR THE USER TO CHOOSE FROM DIFFERENT LANGUAGES
3 - MAKE RESIZING OF GUI POSSIBLE ----> DONE
4 - ADD FEATURE TO LET USER CHOOSE WHAT DIFFICULTY HE/SHE WANTS
5 - Add Zoom in/out
6 - ADD ANIMATION TO THE HANGMAN

TODO BUGS NEED TO BE FIXED:

1 - SOMETIMES WHEN INPUT OF KEYBOARD IS TOO FAST, SOME LINES DON'T GET DRAWN WHEN WRONG LETTER
    IS TYPED IN (NOT NECESSARY FOR NOW)
2 - BLOCK KEYBOARD/MOUSE INPUT (with PyHook lib) WHEN GAME IS LOST OR WON FOR A BIT AND THEN ENABLE IT AGAIN
    WHEN THE GAME IS RESTARTED (NECESSARY)
'''

# Init the pygame modules and name of the game
# pygame.init()
# screenSizeInfo = pygame.display.Info()

# pygame.display.set_caption('Hangman Game')

# SAVE_FILE = "data (do not modify)/save_file"
# checksum_file_name = "data (do not modify)/checksum"
# words_file_name = "data (do not modify)/nl_words" # TODO: change this to en_words

# BUF_SIZE: to read 64kb chunks at a time for digest
# BUF_SIZE = 65536

# setting font type
# Font = pygame.font.Font("freesansbold.ttf", 33)
# FontArial = pygame.font.Font("freesansbold.ttf", 25)

# color vars
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)
# RED = (255, 0, 0)
# GREEN = (0, 100, 0)
# # BLUE = (0, 0, 255)
# BLUE = (25, 25, 112)
# GREY = (200, 200, 200)

# def show_background():
#     # Setting width and height of the GUI (params have to be tuples so NOT list or separate numbers
#     # inputted in the setmode func.
#     gameDisplay = pygame.display.set_mode((795, 450), RESIZABLE)
#     gameDisplay.fill(RGBColor.GREY.value)
#     pygame.display.update()
# show_background()

# amount of correctly guessed words
# GUESSED_WORDS = 0

# amount of incorrectly guesses words
# incorrect_guesses = 0

# init used_words
# used_words = []

# LINE = None

# sha256 hash for checking the save_file integrity
# def sha256_hash_digest(file_name_to_hash=SAVE_FILE):
#     global BUF_SIZE

#     # the hash
#     sha256_hash = hashlib.sha256()

#     with open(file_name_to_hash, 'rb') as sf:
#         while True:
#             data = sf.read(BUF_SIZE)
#             if not data:
#                 break
#             sha256_hash.update(data)

#     return sha256_hash.hexdigest()


# checking for file integrity
# def sha256_hash_check(file_to_check, checksum):
#     hash_digested = sha256_hash_digest(file_to_check)

#     if checksum == hash_digested:
#         return True
#     else:
#         return False


# def saving_progress(used_words_arr, correctly_guessed_words, incorrectly_guessed_words):
#     # removing last word that was mistakenly added
#     del used_words_arr[len(used_words_arr)-1]

#     try:
#         with open(save_file_name, "w") as f:

#             f.write(','.join(used_words_arr) + '\n')
#             f.write(str(correctly_guessed_words) + '\n')
#             f.write(str(incorrectly_guessed_words))
#             print("saved progress successfully!")

#         with open(checksum_file_name, "w") as checksum_file:
#             checksum_file.write(sha256_hash_digest(save_file_name))

#     except ValueError:
#         Tk().wm_withdraw()  # to hide the main window
#         messagebox.showerror('CAN\'T CREATE SAVE FILE',
#                              'Please notify the creator of this game to solve this problem.')
#         pygame.quit()
#         quit()


# def delete_save_file(name_of_savefile, checksum_file):

#     if os.path.exists(name_of_savefile) and os.path.exists(checksum_file):
#         os.remove(name_of_savefile)
#         os.remove(checksum_file)
#         messagebox.showinfo('SAVE FILES DELETED',
#                              'Save files deleted successfully.')
#     else:
#         Tk().wm_withdraw()  # to hide the main window
#         messagebox.showerror('CAN\'T DELETE SAVE FILE',
#                              'There are no save files to be deleted.')

#     pygame.quit()
#     quit()


# if save file exists in root folder, set guessed_words, incorrect_guesses and
# used_words to those values. If no save file exists then set everything to default values
# def load_save_file():
#     global used_words, GUESSED_WORDS, incorrect_guesses

#     try:
#         with open(save_file_name, 'r') as file:

#             with open(checksum_file_name, 'r') as get_checksum:
#                 the_checksum = get_checksum.readline()

#                 if sha256_hash_check(save_file_name, the_checksum):
#                     pass
#                 else:
#                     Tk().wm_withdraw()  # to hide the main window
#                     messagebox.showerror('HASH UNMATCH FOUND', "Save File has been tempered with! Exiting Game ...")
#                     pygame.quit()
#                     quit()

#             first_line = file.readline()

#             # checking whether the first line is empty (this causes reading issues)
#             # thus checking for it is necessary for stable file reading
#             if first_line == "\n":
#                 pass
#             else:
#                 used_words = [x.strip() for x in first_line.split(',')]

#             GUESSED_WORDS = int(file.readline().replace("\n", "").replace(",", ""))
#             incorrect_guesses = int(file.readline())

#             return True

#     except FileNotFoundError:
#         Tk().wm_withdraw()  # to hide the main window
#         messagebox.showerror('NO SAVE FILES FOUND', 'No save files found called \'save_file\'. '
#                                                     'All game variables are set to default values. '
#                                                     'Please click \'ok\' to continue to the game. ')

#     except ValueError:
#         Tk().wm_withdraw()  # to hide the main window
#         messagebox.showerror('CAN\'T READ SAVE FILE', 'Please remove all changes done to save file and checksum '
#                                                       'file, check whether the file extension of both checksum and save file are ".file"'
#                                                       ' or delete the save file to be able to start the game')
#         pygame.quit()
#         quit()


# if os.path.isfile(save_file_name):
#     # asking user whether he/she wants to load the save file
#     Tk().wm_withdraw()  # to hide the main window
#     msg = messagebox.askquestion('LOAD SAVE FILE?', 'Do you want to load your save file?', icon='warning')
#     if msg == 'yes':
#         if load_save_file():
#             Tk().wm_withdraw()
#             msg = messagebox.showinfo('CONFIRMATION MESSAGE', 'SAVE FILE LOADED SUCCESSFULLY!')
#         else:
#             msg = messagebox.showinfo('ERROR MESSAGE', 'SOMETHING UNEXPECTED HAPPENED WHILE LOADING THE SAVE FILE!'
#                                                        'PLEASE NOTIFY ADMIN ABOUT THIS ERROR.')
#             pygame.quit()
#             quit()

'''
opening the file once and read the word from it
replaced try/except snippet from main() to here
so that the file gets opened once and not every time main() gets called
(this of course for efficiency)
'''
# def getting_words():
#     """Opening the wordlist and assign it to the global var to read it later
#     """
#     global LINE
#     try:
#         with open(words_file_name, "r") as words_file:
#             LINE = words_file.read().splitlines()
#             # return line
#     except IOError:
#         Tk().wm_withdraw()  # to hide the main window
#         messagebox.showerror('WORDSLIST NOT FOUND!', 'Words list of the game is missing! Try to re-download the wordslist '
#                                                     'from the download link of the game.')
#         pygame.quit()
#         quit()
# getting_words()

# '''
# function for drawing hangman lines
# '''
# def hangman_states(condition):

#     if condition == 0:
#         pygame.draw.line(gameDisplay, BLACK, (10, 400), (300, 400), 8)  # baseline
#         pygame.draw.line(gameDisplay, BLACK, (50, 50), (50, 400), 8)  # stick1
#         pygame.draw.line(gameDisplay, BLACK, (50, 60), (250, 60), 8)  # stick2
#         pygame.draw.line(gameDisplay, BLACK, (150, 60), (150, 100), 8)  # rope
#         pygame.draw.circle(gameDisplay, BLACK, (150, 150), 50, 8)  # head
#         pygame.draw.line(gameDisplay, BLACK, (150, 200), (150, 300), 8)  # body
#         pygame.draw.line(gameDisplay, BLACK, (150, 210), (100, 250), 8)  # lefthand
#         pygame.draw.line(gameDisplay, BLACK, (150, 210), (200, 250), 8)  # righthand
#         pygame.draw.line(gameDisplay, BLACK, (150, 300), (100, 350), 8)  # leftleg
#         pygame.draw.line(gameDisplay, BLACK, (150, 300), (200, 350), 8)  # rightleg

#     elif condition == 1:
#         pygame.draw.line(gameDisplay, RED, (10, 400), (300, 400), 8)  # baseline

#     elif condition == 2:
#         pygame.draw.line(gameDisplay, RED, (50, 50), (50, 400), 8)  # stick1

#     elif condition == 3:
#         pygame.draw.line(gameDisplay, RED, (50, 60), (250, 60), 8)  # stick2

#     elif condition == 4:
#         pygame.draw.line(gameDisplay, RED, (150, 60), (150, 100), 8)  # rope

#     elif condition == 5:
#         pygame.draw.circle(gameDisplay, RED, (150, 150), 50, 8)  # head

#     elif condition == 6:
#         pygame.draw.line(gameDisplay, RED, (150, 200), (150, 300), 8)  # body

#     elif condition == 7:
#         pygame.draw.line(gameDisplay, RED, (150, 210), (100, 250), 8)  # lefthand

#     elif condition == 8:
#         pygame.draw.line(gameDisplay, RED, (150, 210), (200, 250), 8)  # righthand

#     elif condition == 9:
#         pygame.draw.line(gameDisplay, RED, (150, 300), (100, 350), 8)  # leftleg

#     elif condition == 10:
#         pygame.draw.line(gameDisplay, RED, (150, 300), (200, 350), 8)  # rightleg

#     # At this point the game is over
#     elif condition == 11:
#         pygame.draw.line(gameDisplay, BLUE, (10, 400), (300, 400), 8)  # baseline
#         pygame.draw.line(gameDisplay, BLUE, (50, 50), (50, 400), 8)  # stick1
#         pygame.draw.line(gameDisplay, BLUE, (50, 60), (250, 60), 8)  # stick2
#         pygame.draw.line(gameDisplay, BLUE, (150, 60), (150, 100), 8)  # rope
#         pygame.draw.circle(gameDisplay, BLUE, (150, 150), 50, 8)  # head
#         pygame.draw.line(gameDisplay, BLUE, (150, 200), (150, 300), 8)  # body
#         pygame.draw.line(gameDisplay, BLUE, (150, 210), (100, 250), 8)  # lefthand
#         pygame.draw.line(gameDisplay, BLUE, (150, 210), (200, 250), 8)  # righthand
#         pygame.draw.line(gameDisplay, BLUE, (150, 300), (100, 350), 8)  # leftleg
#         pygame.draw.line(gameDisplay, BLUE, (150, 300), (200, 350), 8)  # rightleg


# def show_word(word_array):

#     # draw white rect to prevent chaos of multiple layers above each other of the word
#     # this is needed for smooth transitions of ASCII
#     pygame.draw.rect(gameDisplay, GREY, (240, 210, 550, 80))

#     display_text_and_blit(gameDisplay, " ".join(word_array), Font, BLACK, 523, 250)


# '''
# creates text and centers its rectangle at (x, y)
# return array with the text and its rectangle (necessary for blit function)
# '''
# def display_text_and_blit(display, text, font, color, x, y):
#     text_msg = font.render(text, True, color)
#     text_msg_rect = text_msg.get_rect()
#     text_msg_rect.center = (x, y)
#     display.blit(text_msg, text_msg_rect)


# def ask_for_saving_file_handler(correctly_guessed_words, incorrectly_guessed_words):
#     gameDisplay.fill(GREY)

#     display_text_and_blit(gameDisplay, "SAVE PROGRESS?",
#                           FontArial, RED, 387, 190)
#     # display_text_and_blit(gameDisplay, "CLICK YES, OTHERWISE CLICK NO", FontArial, BLACK, 387, 230)

#     # rect for YES
#     yes_rect = pygame.draw.rect(gameDisplay, BLUE, (220, 245, 75, 55))
#     gameDisplay.blit(FontArial.render('YES', True, (255, 0, 0)), (230, 260))

#     # rect for NO
#     no_rect = pygame.draw.rect(gameDisplay, BLUE, (457, 245, 75, 55))
#     gameDisplay.blit(FontArial.render('NO', True, (255, 0, 0)), (474, 260))

#     pygame.display.update()

#     while True:
#         for event in pygame.event.get():

#             if event.type == pygame.QUIT:
#                 Tk().wm_withdraw()  # to hide the main window
#                 msg_progress_not_saved = messagebox.askquestion('WARNING: PROGRESS NOT SAVED!', 'Your progress isn\'t saved. Do you really want '
#                                                                 'to quit without saving progress?', icon='warning')
#                 if msg_progress_not_saved == 'yes':
#                     pygame.quit()
#                     quit()

#             if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
#                 mouse_pos = pygame.mouse.get_pos()

#                 if yes_rect.collidepoint(mouse_pos):
#                     saving_progress(
#                         used_words, correctly_guessed_words, incorrectly_guessed_words)

#                     gameDisplay.fill(GREY)

#                     display_text_and_blit(
#                         gameDisplay, "PROGRESS SAVED SUCCESSFULLY!", FontArial, RED, 387, 190)
#                     pygame.display.update()
#                     time.sleep(0.5)

#                     display_text_and_blit(
#                         gameDisplay, "EXITING GAME ...", FontArial, BLACK, 387, 230)
#                     pygame.display.update()
#                     time.sleep(0.25)

#                     pygame.quit()
#                     quit()

#                 if no_rect.collidepoint(mouse_pos):

#                     Tk().wm_withdraw()  # to hide the main window
#                     msg_progress_not_saved = messagebox.askquestion('WARNING!!!',
#                                                                     'You are about to exit the game without saving! '
#                                                                     'Are you sure you DON\'T want to save your progress?')
#                     if msg_progress_not_saved == 'yes':
#                         pygame.quit()
#                         quit()


# def main(guessed_words, incorrect_guesses):
# take a random word from the words file
# word = random.choice(LINE)

# # preventing infinite loop when all words are used
# if len(used_words) == len(LINE):
#     gameDisplay.fill(GREY)

#     Tk().wm_withdraw()  # to hide the main window
#     msg_progress_not_saved = messagebox.askquestion('ALL WORDS ARE USED',
#                                                     'Do you want to DELETE save files?')
#     if msg_progress_not_saved == 'yes':
#         global save_file_name, checksum_file_name
#         delete_save_file(save_file_name, checksum_file_name)
#     else:
#         pygame.quit()
#         quit()

# while True:
#     # choose word that has not already been used
#     if word in used_words:
#         word = random.choice(LINE)
#         continue

#     break

# append the new word so that it doesn't get used anymore
# used_words.append(word)

# # length of the word
# length_word = len(word)

# # array of the word chosen
# arr_of_the_word = []

# # array for used letters of the chosen word
# used_letters = []

# # fill the list with blank chars
# for i in range(length_word):
#     arr_of_the_word.append("_ ")

# show_word(arr_of_the_word)

# # state of hangman character
# cond = 0

# # var to check whether the word has been guessed or the game is over
# word_bool = False

# show_info_and_statistics(guessed_words, incorrect_guesses)

# try:
#     # while not gameExit:
#     while True:
#         pygame.event.pump()

#         # draw initial hang man character
#         hangman_states(cond)

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 ask_for_saving_file_handler(
#                     guessed_words, incorrect_guesses)

#             # Make resizing of the game windows possible
#             elif event.type == pygame.VIDEORESIZE:
#                 width, height = event.dict['size']

#                 if (width, height) == (screenSizeInfo.current_w, screenSizeInfo.current_h):
#                     width = 795
#                     height = 450

#                 print(width, " ", height)
#                 print("FULLSCREEN: ", pygame.FULLSCREEN)

#                 # limiting resizing width and height
#                 if width < 775 or width > 830:
#                     width = 795

#                 if height != 450:
#                     height = 450

#                 pygame.display.set_mode((width, height), RESIZABLE)
#                 gameDisplay.fill(GREY)

#                 show_word(arr_of_the_word)

#                 hangman_states(0)

#                 for condition in range(cond, 0, -1):
#                     hangman_states(condition)

#                 show_info_and_statistics(guessed_words, incorrect_guesses)

#             elif event.type == pygame.KEYDOWN:

#                 # exiting the game
#                 if event.key == pygame.K_0 or event.key == pygame.K_KP0:
#                     ask_for_saving_file_handler(
#                         guessed_words, incorrect_guesses)

#                 # handling case where user wants a hint
#                 elif event.key == pygame.K_1 or event.key == pygame.K_KP1:

#                     # choosing a letter that has not yet been guessed in the word
#                     while True:
#                         letter_of_hint = random.choice(word)
#                         if letter_of_hint in arr_of_the_word:
#                             continue

#                         break

#                     # append the letter to the array of the letters of the word
#                     for i in range(length_word):
#                         if word[i] == letter_of_hint:
#                             arr_of_the_word[i] = letter_of_hint
#                             used_letters.append(letter_of_hint)

#                     # make the hinted letter appear
#                     show_word(arr_of_the_word)

#                 # Check whether the guessed letter is present in the word
#                 elif re.search("[a-zA-Z]", chr(event.key)):

#                     if ((chr(event.key).upper() in word) or (chr(event.key).lower() in word)) \
#                             and (chr(event.key) not in arr_of_the_word):
#                         for i in range(length_word):
#                             if (word[i] == (chr(event.key)).upper()) or (word[i] == (chr(event.key)).lower()):
#                                 arr_of_the_word[i] = word[i]

#                     else:
#                         # check whether the letter has already been used, if not then store it in used words array and count
#                         # it as wrong letter
#                         if (chr(event.key) in used_letters) or (chr(event.key) in arr_of_the_word):
#                             display_text_and_blit(gameDisplay, "ALREADY USED LETTER " + chr(event.key).upper(), FontArial, RED, 500,
#                                                   100)
#                         else:
#                             # if ticked letter is not in the word and not used before
#                             used_letters.append(chr(event.key))
#                             cond = cond + 1

#                     show_word(arr_of_the_word)

#                     # to make some time to draw line
#                     time.sleep(0.05)

#                 else:
#                     display_text_and_blit(
#                         gameDisplay, "INVALID INPUT!", FontArial, RED, 500, 100)

#             # hide invalid input msg after it appears
#             elif event.type == pygame.KEYUP:
#                 pygame.draw.rect(gameDisplay, GREY, (260, 50, 500, 100))

#         # handling case where the user wasn't able to guess the word
#         if cond == 10:
#             gameDisplay.fill(GREY)
#             hangman_states(cond + 1)

#             display_text_and_blit(gameDisplay, "YOU LOST!", Font, RED, 450,
#                                   250)

#             display_text_and_blit(gameDisplay, "The words is:", Font, GREEN, 450,
#                                   285)

#             display_text_and_blit(gameDisplay, word, Font, BLACK, 450,
#                                   318)

#             incorrect_guesses += 1

#             word_bool = True

#         # handling case where the user was able to guess the word
#         elif "".join(arr_of_the_word) == word:
#             gameDisplay.fill(GREY)

#             display_text_and_blit(gameDisplay, "YOU GUESSED THE RIGHT WORD!", Font, GREEN, 400,
#                                   220)

#             display_text_and_blit(gameDisplay, "The word is:", Font, GREEN, 400,
#                                   250)

#             display_text_and_blit(gameDisplay, word, Font, BLACK, 400,
#                                   285)

#             guessed_words += 1

#             word_bool = True

#         pygame.display.update()
#         pygame.time.Clock().tick(30)  # 30fps

#         if word_bool is True:
#             time.sleep(1)
#             gameDisplay.fill(GREY)
#             main(guessed_words, incorrect_guesses)
# except Exception as e:
#     print(e)

# if __name__ == "__main__":
#     main(guessed_words, incorrect_guesses)
