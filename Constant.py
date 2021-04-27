from pygame import *
from stockfish import *
from Text import Text
from GameButton import GameButton
from Server import *
from Client import *

# game screen window
screen = display.set_mode((603, 783))
display.set_caption("Chess of Chaos")
# display.set_icon(image.load("images\\game_icon.jpg"))

# images
pieces_img = image.load("images\\figures.png")
board_img = image.load("images\\board0.png")
game_background = image.load("images\\menu_background.jpg")
game_background = transform.scale(game_background, (603, 483))
start_button_img = image.load("images\\start_button.png")
exit_button_img = image.load("images\\exit_button.png")
host_button_img = image.load("images\\host_button.png")
join_button_img = image.load("images\\join_button.png")
play_button_img = image.load("images\\play_button.png")
find_button_img = image.load("images\\find_button.png")
lock_in_button_img = image.load("images\\lock_in_button.png")

# chess engine
engine = Stockfish(path="stock_fish.exe", depth=18, parameters=None)

# game properties
host_net = Server()
join_server = Client()

SIZE = 56
game_offset = Vector2(0, 165)
board = [[0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0]]
pieces = []
piece_sequence = [-6, -2, -3, -1, -4, -5, 6, 2, 3, 1, 4, 5]
piece_letter = {
    1: 'R', -1: 'r',
    2: 'N', -2: 'n',
    3: 'B', -3: 'b',
    4: 'Q', -4: 'q',
    5: 'K', -5: 'k',
    6: 'P', -6: 'p'
}
piece_value = {
    1: 4,
    2: 3,
    3: 3,
    4: 7,
    5: 0,
    6: 1
}
castle_moves = {
    "e1g1": "h1f1",
    "e1c1": "a1d1",
    "e8g8": "h8f8",
    "e8c8": "a8d8"
}

# colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 128)
title_color = (48, 83, 198)
grey = (150, 150, 150)

# texts
text_font = font.Font('Good Unicorn - TTF.ttf', 30)
big_text_font = font.Font('Good Unicorn - TTF.ttf', 190)
menu_text_font = font.Font('Good Unicorn - TTF.ttf', 70)
_font = font.Font('Good Unicorn - TTF.ttf', 35)

white_texts = [Text("Money:", text_font, Vector2(500, 660), white),
               Text("1", text_font, Vector2(38, 760), white),
               Text("3", text_font, Vector2(105, 760), white),
               Text("3", text_font, Vector2(170, 760), white),
               Text("4", text_font, Vector2(237, 760), white),
               Text("7", text_font, Vector2(302, 760), white),
               Text("0", text_font, Vector2(368, 760), white)]
black_texts = [Text("Money:", text_font, Vector2(500, 120), white),
               Text("1", text_font, Vector2(38, 100), white),
               Text("3", text_font, Vector2(105, 100), white),
               Text("3", text_font, Vector2(170, 100), white),
               Text("4", text_font, Vector2(237, 100), white),
               Text("7", text_font, Vector2(302, 100), white),
               Text("0", text_font, Vector2(368, 100), white)]
game_title = Text("CHESS OF CHAOS", menu_text_font, Vector2(300, 100), title_color)

# Game Button
start_button = GameButton(start_button_img, 350, 212, 70)
exit_button = GameButton(exit_button_img, 400, 145, 70)
host_button = GameButton(host_button_img, 200, 180, 70)
join_button = GameButton(join_button_img, 300, 163, 70)
play_button = GameButton(play_button_img, 300, 183, 70)
find_button = GameButton(find_button_img, 300, 160, 70)
lock_in_button = GameButton(lock_in_button_img, 380, 145, 35)
lock_in_button.rect.x = 455
