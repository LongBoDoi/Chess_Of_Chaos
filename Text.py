import pygame
import Constant

pygame.init()


class Text:
    text = None
    text_Rect = None

    def __init__(self, text, font, center, color):
        self.text = font.render(text, True, color, None)
        self.text_Rect = self.text.get_rect()
        self.text_Rect.center = center

    def render(self):
        Constant.screen.blit(self.text, self.text_Rect)
