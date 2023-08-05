import pygame as pg

from PGUI.uielement import UIElement

def loadify(imgname, size: tuple[int, int] = None, colour_key: tuple[int, int, int] = None):
    image = pg.image.load(imgname).convert_alpha()
    if size:
        image = pg.transform.scale(image, size)
    if colour_key:
        image.set_colorkey(colour_key)
    return image

class Image(UIElement):
    def __init__(
            self, window,
            x: int, y: int, 
            width: int, height: int,
            image_source: str, image: pg.image = None
        ):
        super().__init__(window, x, y, width, height)

        self.image_source = image_source
        self.image = image


    def draw(self):
        super().draw()
        if self.image == None:
            image = self.loadify(self.image_source)
            self.image = pg.transform.scale(image, (self.width, self.height))

        self.window.screen.blit(self.image, (self.x, self.y))
        
