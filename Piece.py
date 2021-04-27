from Constant import *


class Piece:
    p_type = None
    value = None
    x = None
    y = None
    width = None
    height = None
    image = None
    is_model_piece = None

    def __init__(self, p_type, location, is_model_piece):
        self.width = SIZE
        self.height = SIZE
        self.p_type = p_type
        self.value = piece_value[abs(self.p_type)]
        self.x, self.y = location
        self.image = pieces_img.subsurface((SIZE * (abs(self.p_type) - 1), SIZE * (1 if self.p_type > 0 else 0),
                                            SIZE, SIZE))
        self.is_model_piece = is_model_piece

    def set_type(self, p_type):
        self.p_type = p_type
        self.image = pieces_img.subsurface((SIZE * (abs(self.p_type) - 1), SIZE * (1 if self.p_type > 0 else 0),
                                            SIZE, SIZE))

    def get_image(self):
        return self.image

    def set_location(self, v):
        self.x = v.x
        self.y = v.y

    def get_location(self):
        return Vector2(self.x, self.y)

    def draw(self):
        screen.blit(self.image, (self.x, self.y + game_offset.y, self.width, self.height))

    def contains_mouse(self, mouse_pos):
        return Rect(self.x, self.y, self.width, self.height).contains(Rect(mouse_pos.x, mouse_pos.y,
                                                                           0, 0))
