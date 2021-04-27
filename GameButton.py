from pygame import Rect, transform
import Constant


class GameButton:
    rect = None
    unselected_img = None
    selected_img = None

    def __init__(self, image, y, width, height):
        self.rect = Rect((603 - width) / 2, y, width, height / 2)
        self.unselected_img = image.subsurface((0, 0, width, height))
        self.selected_img = image.subsurface((0, height, width, height))
        self.unselected_img = transform.scale(self.unselected_img, (width, int(height / 2)))
        self.selected_img = transform.scale(self.selected_img, (width, int(height / 2)))
        self.is_selected = False

    def contains_mouse(self, mouse_pos):
        return self.rect.contains((mouse_pos.x, mouse_pos.y, 0, 0))

    def render(self, mouse_pos):
        Constant.screen.blit(self.selected_img if self.contains_mouse(mouse_pos) else self.unselected_img, self.rect)
