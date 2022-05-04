#imports
from settings import *
import pygame as pg
vec = pg.math.Vector2

class KingTower(pg.sprite.Sprite):
    def __init__(self, game, x, y, group):
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((75,75))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x,y)

        self.hp = 1000

class ArcherTower(pg.sprite.Sprite):
    def __init__(self, game, x, y, group):
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((75, 75))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = vec(x, y)

        self.hp = 1000