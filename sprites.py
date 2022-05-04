#imports
import math

from settings import *
import pygame as pg
vec = pg.math.Vector2

class KingTower(pg.sprite.Sprite):
    def __init__(self, game, x, y, group):
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((KING_SIZE,KING_SIZE))
        self.image.fill(RED)
        self.width = KING_SIZE
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = (self.pos)

        self.hp = 1000

class ArcherTower(pg.sprite.Sprite):
    def __init__(self, game, x, y, group):
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((ARCHER_SIZE, ARCHER_SIZE))
        self.image.fill(GREEN)
        self.width = ARCHER_SIZE
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = (self.pos)
        self.hp = 500

class Troop(pg.sprite.Sprite):
    def __init__(self, game, x, y, group):
        self.groups = game.all_sprites, group
        self.enemyTowers = game.enemyTowers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((25, 25))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = (self.pos)

        self.hp = 100
        self.damage = 50
        self.target = None



    #calculate the distance between troop and towers and choose closest one
    def calcDistance(self):
        towers = []
        towerDist = []
        for tower in self.enemyTowers:
            dist = math.sqrt((self.pos.x - tower.pos.x)**2 + (self.pos.y - tower.pos.y)**2)
            towerDist.append(dist)
            towers.append(tower)
        # if king tower is closest
        if towerDist[0] < towerDist[1] and towerDist[2]:
            self.target = towers[0]
        # if left tower is closest
        elif towerDist[1] < towerDist[0] and towerDist[2]:
            self.target = towers[1]
        # if right tower is closest
        elif towerDist[2] < towerDist[0] and towerDist[1]:
            self.target = towers[2]

    def update(self):
        self.calcDistance()
        if self.pos.x > self.target.pos.x:
            self.pos.x -= TROOP_SPEED
        if self.pos.y > (self.target.pos.y + (self.target.width / 1.5)):
            self.pos.y -= TROOP_SPEED
        self.rect.center = self.pos