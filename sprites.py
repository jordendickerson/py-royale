#imports
import math

from settings import *
import pygame as pg
vec = pg.math.Vector2

def move(self, speed):
    # move troop if not at tower x
    if self.pos.x != self.target.pos.x:
        # check which side of the tower it is on
        if self.pos.x > self.target.pos.x:
            self.pos.x -= speed
        else:
            self.pos.x += speed
    # move troop if not at tower y
    if self.pos.y != self.target.pos.y:
        # check which side of the tower it is on
        if self.pos.y > self.target.pos.y:
            self.pos.y -= speed
        else:
            self.pos.y += speed
    self.rect.center = self.pos
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
        self.target = None
        self.targetInRange = False

    def findTarget(self):
        troops = []
        troopDist = []
        #add distance from all troops to a list
        for troop in self.game.troops:
            dist = math.sqrt((self.pos.x - troop.pos.x) ** 2 + (self.pos.y - troop.pos.y) ** 2)
            troops.append(troop)
            troopDist.append(dist)
        #set minimum distance
        minDist = troopDist.index(min(troopDist))
        #set target to closest troop
        self.target = troops[minDist]
        #check if target is close enough to shoot
        targetDist = math.sqrt((self.target.pos.x - self.pos.x) ** 2 + (self.target.pos.y - self.pos.y) ** 2)
        if targetDist < 175:
            self.targetInRange = True
        else:
            pass
            self.targetInRange = False

    def shoot(self):
        Arrow(self.game, self.pos.x, self.pos.y, self.game.arrows, self.target)

    def update(self):
        self.findTarget()
        if self.targetInRange:
            self.shoot()
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
        # checks for collision with tower
        hits = pg.sprite.spritecollide(self, self.enemyTowers, False)
        if not hits:
            move(self, TROOP_SPEED)
        else:
            self.timeSince += self.game.dt
            if self.timeSince > 1500:
                self.attackTarget()
                self.timeSince = 0
            self.rect.center = self.rect.center
        # kill if hp runs out
        if self.hp <= 0:
            self.kill()

class Arrow(pg.sprite.Sprite):
    def __init__(self, game, x, y, group, target):
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(BLACK)
        self.width = ARCHER_SIZE
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = (self.pos)
        self.target = target

    def update(self):
        move(self, ARROW_SPEED)
