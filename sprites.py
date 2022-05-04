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

        self.hp = KING_HP

    def update(self):
        #kill if hp runs out
        if self.hp <= 0:
            self.kill()

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
        self.hp = ARCHER_HP

    def update(self):
        #kill if hp runs out
        if self.hp <= 0:
            self.kill()

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

        self.hp = TROOP_HP
        self.damage = TROOP_DAMAGE
        self.target = None
        self.timeSince = 0



    #calculate the distance between troop and towers and choose closest one
    def calcDistance(self):
        towers = []
        towerDist = []
        #go through every tower in the enemy towers group
        for tower in self.enemyTowers:
            dist = math.sqrt((self.pos.x - tower.pos.x)**2 + (self.pos.y - tower.pos.y)**2)
            towerDist.append(dist) #append the distance from the tower to the tower distance list
            towers.append(tower) #append the tower to the towers list
        try:
            #find the index of closest tower in towers list
            minIndex = towerDist.index(min(towerDist))
            #set target to the minIndex from towers
            self.target = towers[minIndex]
        except:
            print('no')
    #attack target if colliding
    def attackTarget(self):
        hits = pg.sprite.spritecollide(self, self.game.enemyTowers, False)
        if hits:
            self.target.hp -= self.damage
            print(self.target.hp)

    def update(self):
        self.calcDistance()
        hits = pg.sprite.spritecollide(self, self.enemyTowers, False)
        if not hits:
            #move troop if not at tower x
            if self.pos.x != self.target.pos.x:
                #check which side of the tower it is on
                if self.pos.x > self.target.pos.x:
                    self.pos.x -= TROOP_SPEED
                else:
                    self.pos.x += TROOP_SPEED
            #move troop if not at tower y
            if self.pos.y != self.target.pos.y:
                # check which side of the tower it is on
                if self.pos.y > self.target.pos.y:
                    self.pos.y -= TROOP_SPEED
                else:
                    self.pos.y += TROOP_SPEED
            self.rect.center = self.pos
        else:
            self.timeSince += self.game.dt
            if self.timeSince > 1500:
                self.attackTarget()
                self.timeSince = 0
            self.rect.center = self.rect.center
