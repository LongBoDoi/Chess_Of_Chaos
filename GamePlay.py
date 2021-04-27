from Piece import *
from Constant import *
import random


def load_position(is_white):
    # clear old board
    for i in range(8):
        for j in range(8):
            board[i][j] = 0
    pieces.clear()

    for t1 in range(6, 12) if is_white else range(6):
        y_row = -145 if piece_sequence[t1] < 0 else 518
        pieces.append(Piece(piece_sequence[t1], Vector2((SIZE + 10) * (t1 % 6) + 10, y_row), True))


def chess_note(pos):
    s = ""
    s += chr(int(pos.x / SIZE) + 97)  # get column letter
    s += chr(int(7 - pos.y / SIZE) + 49)  # get row number
    return s


def to_coord(a, b):
    x1 = ord(a) - 97  # get column number from letter
    y1 = 7 - ord(b) + 49  # get row number
    return Vector2(x1 * SIZE, y1 * SIZE)


def draw_images(is_white):
    screen.fill(black)
    screen.blit(board_img, (board_img.get_rect().x, board_img.get_rect().y + game_offset.y))
    for p in pieces:
        p.draw()
    for text in white_texts if is_white else black_texts:
        text.render()


def correctly_placed(piece_selected, pos, money):
    if money < piece_selected.value:
        return False

    # pawn can only be placed on 2nd or 3rd rank
    if piece_selected.p_type == 6:
        pawn_num = 0
        for i in range(5, 7):
            for j in range(8):
                if board[i][j] == 6:
                    pawn_num += 1
        if pawn_num == 10 and piece_selected.is_model_piece:
            return False
        else:
            return pos.y / 56 in range(5, 7)
    if piece_selected.p_type == -6:
        pawn_num = 0
        for i in range(1, 3):
            for j in range(8):
                if board[i][j] == -6:
                    pawn_num += 1
        if pawn_num == 10 and piece_selected.is_model_piece:
            return False
        return pos.y / 56 in range(1, 3)

    # other pieces can only be placed on 1st or 2nd rank
    if piece_selected.p_type in range(1, 6):
        # players can only have one king
        if piece_selected.p_type == 5 and piece_selected.is_model_piece:
            for i in range(6, 8):
                for j in range(8):
                    if board[i][j] == 5:
                        return False
        return pos.y / 56 in range(6, 8)
    if piece_selected.p_type in range(-5, 0):
        if piece_selected.p_type == -5 and piece_selected.is_model_piece:
            for i in range(0, 2):
                for j in range(8):
                    if board[i][j] == -5:
                        return False
        return pos.y / 56 in range(0, 2)


class GamePlay:
    direction = None  # for drawing pieces position
    mouse_pos = None  # mouse position

    # for FEN position
    moves = None
    en_passant = None
    half_moves = None
    # castle abilities
    white_o_o = None
    white_o_o_o = None
    black_o_o = None
    black_o_o_o = None

    is_white = None
    is_host = None
    money = None
    money_text = None

    def __init__(self, is_white, is_host):
        self.moves = 0
        self.en_passant = ""
        self.half_moves = 0
        self.white_o_o = None
        self.black_o_o = None
        self.white_o_o_o = None
        self.black_o_o_o = None
        self.is_white = is_white
        self.is_host = is_host
        self.money = 35
        self.money_text = text_font.render(str(self.money), True, white)

        load_position(self.is_white)

        self.prepare_stage()

    def move(self, move_note, move_piece):
        old_pos_1 = to_coord(move_note[0], move_note[1])
        new_pos_1 = to_coord(move_note[2], move_note[3])
        if old_pos_1 == new_pos_1:  # for debugging, avoid deleting the same piece
            return
        if new_pos_1.x / SIZE not in range(0, 8) or new_pos_1.y / SIZE not in range(0, 8):
            return

        capture = False
        pawn_advanced = False
        # for half_moves

        for p in pieces:
            if p.get_location() == old_pos_1:
                move_piece = p
            if p.get_location() == new_pos_1 and not p.is_model_piece:
                pieces.remove(p)  # if there is a piece in the new position, that piece will be taken
                capture = True
                self.money += p.value
                self.money_text = text_font.render(str(self.money), True, white)

        if move_piece is not None:
            if move_piece.p_type == 6 or move_piece.p_type == -6:
                pawn_advanced = True
                # en_passant
                if move_note[0] == move_note[2] and move_note[1] == "2" and move_note[3] == "4":
                    self.en_passant = move_note[0] + str(3)
                if move_note[0] == move_note[2] and move_note[1] == "7" and move_note[3] == "5":
                    self.en_passant = move_note[0] + str(6)
                # promotion
                if move_note[3] == "1":
                    move_piece.set_type(-4)
                if move_note[3] == "8":
                    move_piece.set_type(4)

            # castle
            if move_piece.p_type == 5 or move_piece.p_type == -5:
                if castle_moves.__contains__(move_note):
                    self.move(castle_moves.get(move_note), None)

            # remove the old square value
            if not move_piece.is_model_piece:
                board[int(old_pos_1.y / SIZE)][int(old_pos_1.x / SIZE)] = 0

            # move the piece to new position and set new value
            move_piece.set_location(new_pos_1)
            board[int(new_pos_1.y / SIZE)][int(new_pos_1.x / SIZE)] = move_piece.p_type

        # update half_moves
        if capture or pawn_advanced:
            self.half_moves = 0
        else:
            self.half_moves += 1

    def get_fen_pos_from_board(self):
        final_string = ""
        for row_index in range(8):
            blank_squares = 0
            piece_row = ""
            for col_index in range(8):
                if board[row_index][col_index] == 0:
                    blank_squares += 1
                else:
                    piece_row += str(blank_squares) if blank_squares != 0 else ""
                    piece_row += piece_letter.get(board[row_index][col_index], "")
                    blank_squares = 0
            piece_row += str(blank_squares) if blank_squares != 0 else ""
            final_string += piece_row
            final_string += "/" if row_index != 7 else ""
        final_string += " w " if self.moves % 2 == 0 else " b "

        if board[0][0] != -1:
            self.black_o_o_o = False
        if board[0][7] != -1:
            self.black_o_o = False
        if board[0][4] != -5:
            self.black_o_o = False
            self.black_o_o_o = False
        if board[7][0] != 1:
            self.white_o_o_o = False
        if board[7][7] != 1:
            self.white_o_o = False
        if board[7][4] != 5:
            self.white_o_o = False
            self.white_o_o_o = False

        castle_string = ""
        if self.white_o_o:
            castle_string += "K"
        if self.white_o_o_o:
            castle_string += "Q"
        if self.black_o_o:
            castle_string += "k"
        if self.black_o_o_o:
            castle_string += "q"
        if castle_string == "":
            castle_string = "-"
        final_string += castle_string
        if self.en_passant == "":
            final_string += " - "
        else:
            final_string += " " + self.en_passant + " "
        self.en_passant = ""
        final_string += str(self.half_moves) + " "
        final_string += str(int(self.moves / 2) + 1)
        return final_string

    def prepare_stage(self):
        is_moving = False  # check if player is moving a piece
        piece_selected = None
        direction = None  # offset between mouse position and piece position
        old_pos = None  # old position of the moving piece

        first_menu = True
        while first_menu:
            self.mouse_pos = mouse.get_pos()
            self.mouse_pos -= game_offset

            for g_event in event.get():
                if g_event.type == QUIT:
                    return
                if g_event.type == KEYDOWN:
                    if g_event.key == K_SPACE:
                        self.moves = 0
                        self.en_passant = ""
                        self.half_moves = 0
                        engine.set_fen_position(self.get_fen_pos_from_board())
                        return self.main_battle()
                # left mouse clicked
                if g_event.type == MOUSEBUTTONDOWN:
                    if g_event.button == 1:
                        if lock_in_button.contains_mouse(self.mouse_pos + game_offset):
                            # check the condition to lock in
                            # there must be 6-10 pawns and 1 king...
                            pawn_num = 0
                            king_num = 0
                            for i in (range(5, 8) if self.is_white else range(3)):
                                for j in range(8):
                                    if board[i][j] == (6 if self.is_white else -6):
                                        pawn_num += 1
                                    if board[i][j] == (5 if self.is_white else -5):
                                        king_num += 1

                            # ...and the pawn structure should not make a rectangle
                            pawn_structure = False
                            for i in range(8):
                                if self.is_white:
                                    if board[5][i] == 6 and board[6][i] != 6:
                                        pawn_structure = True
                                    if board[5][i] != 6 and board[6][i] == 6:
                                        pawn_structure = True
                                else:
                                    if board[1][i] == -6 and board[2][i] != -6:
                                        pawn_structure = True
                                    if board[1][i] != -6 and board[2][i] == -6:
                                        pawn_structure = True
                            if pawn_num in range(6, 11) and king_num == 1 and pawn_structure:
                                first_menu = False
                        for piece in pieces:
                            if piece.contains_mouse(self.mouse_pos):
                                is_moving = True
                                piece_selected = piece
                                direction = self.mouse_pos - piece_selected.get_location()
                                old_pos = piece_selected.get_location()

                                # add a new model piece if player clicked it
                                if piece_selected.is_model_piece:
                                    new_piece = Piece(piece.p_type, piece.get_location(), True)
                                    pieces.append(new_piece)
                                break
                # left mouse released
                if g_event.type == MOUSEBUTTONUP:
                    if g_event.button == 1:
                        if piece_selected is None:
                            break

                        # get the new position of the moving piece
                        is_moving = False
                        p = piece_selected.get_location() + Vector2(SIZE / 2, SIZE / 2)
                        new_pos = Vector2(SIZE * int(p.x / SIZE), SIZE * int(p.y / SIZE))

                        if new_pos.x / SIZE not in range(0, 8) or new_pos.y / SIZE not in range(0, 8):
                            # for debugging
                            # there's a chance that the piece will be moved to the row or column right outside
                            # the edge of the board
                            piece_selected.set_location(old_pos)
                            break

                        # if the piece is not placed correctly according to the rule
                        if not correctly_placed(piece_selected, new_pos, 35):
                            piece_selected.set_location(old_pos)
                            break

                        # perform moving the piece to the new position
                        piece_selected.set_location(old_pos)
                        self.move(chess_note(old_pos) + chess_note(new_pos), piece_selected)
                        piece_selected.set_location(new_pos)

                        # subtract the money remaining
                        if piece_selected.is_model_piece:
                            self.money -= piece_selected.value
                            self.money_text = text_font.render(str(self.money), True, white)

                        # after the piece is moved into the board it is no longer a model piece
                        piece_selected.is_model_piece = False
                        piece_selected = None

            if is_moving:
                piece_selected.set_location(self.mouse_pos - direction)

            draw_images(self.is_white)
            screen.blit(self.money_text, dest=(540, 647 if self.is_white else 107))
            lock_in_button.render(self.mouse_pos + game_offset)

            display.flip()

        # when player has locked in
        if self.is_host:
            host_net.send("Locked in")
        else:
            join_server.send("Locked in")
        # send position of pieces to other player
        for i in range(5, 8) if self.is_white else range(3):
            for j in range(8):
                # the value can have 2 letter (negative number) so if it is a positive number
                # add a space after it
                info = str(board[i][j]) + (" " if board[i][j] >= 0 else "")
                if self.is_host:
                    host_net.send(info)
                else:
                    join_server.send(info)

        second_menu = True
        while second_menu:
            for g_event in event.get():
                if g_event.type == QUIT:
                    return

            # get status and position of opponent's pieces
            if self.is_host:
                other_player_status = host_net.receive(9)
            else:
                other_player_status = join_server.receive(9)
            if other_player_status == "Locked in":
                for i in range(3) if self.is_white else range(5, 8):
                    for j in range(8):
                        if self.is_host:
                            p_index = int(host_net.receive(2))
                        else:
                            p_index = int(join_server.receive(2))
                        # set the value to the board and add the piece to that square
                        board[i][j] = p_index
                        if p_index != 0:
                            pieces.append(Piece(p_index, Vector2(j * SIZE, i * SIZE), False))

                return self.main_battle()

            # rendering
            draw_images(self.is_white)

            display.flip()

    def main_battle(self):
        is_turn = self.is_white
        win = None

        first_menu = True
        while first_menu:
            for game_event in event.get():
                if game_event.type == QUIT:
                    return

            if engine.get_evaluation() == {'type': 'mate', 'value': 0}:
                win = not is_turn
                first_menu = False

            # get the move according to player turn
            if is_turn:
                next_move = engine.get_best_move_time(random.randint(0, 1000))
                if next_move is None:
                    continue
                if self.is_host:
                    host_net.send(next_move)
                else:
                    join_server.send(next_move)
                is_turn = not is_turn
            else:
                if self.is_host:
                    next_move = host_net.receive(4)
                else:
                    next_move = join_server.receive(4)
                if next_move == "":
                    continue
                is_turn = not is_turn

            # perform the move and set the board
            old_pos = to_coord(next_move[0], next_move[1])
            new_pos = to_coord(next_move[2], next_move[3])

            moving_piece = None

            for p in pieces:
                if p.get_location() == old_pos:
                    moving_piece = p
                    break

            if moving_piece is None:
                continue

            # animation
            for k in range(26):
                vt = new_pos - old_pos
                screen.blit(board_img, (board_img.get_rect().x, board_img.get_rect().y + game_offset.y))
                for p in pieces:
                    if p == moving_piece:
                        continue
                    p.draw()
                screen.blit(moving_piece.image, (moving_piece.x + (vt.x / 50) * k * 2,
                                                 moving_piece.y + (vt.y / 50) * k * 2 + game_offset.y,
                                                 moving_piece.width, moving_piece.height))
                display.flip()

            self.move(next_move, None)
            self.moves += 1
            # Perform the next move
            engine.set_fen_position(self.get_fen_pos_from_board())
            # Set the board after the move is performed

            draw_images(self.is_white)

            display.flip()

        # When the match is finished
        result = big_text_font.render("VICTORY" if win else "DEFEAT", True, green if win else red)
        second_menu = True
        while second_menu:
            for game_event in event.get():
                if game_event.type == QUIT:
                    return

            draw_images(self.is_white)
            screen.blit(result, dest=((603 - result.get_rect().w) / 2, (783 - result.get_rect().h) / 2))
            display.flip()
