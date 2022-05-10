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

def draw_text(surf, text, size, color, x, y):
    font = pg.font.Font(font_name, size)
    text_surf = font.render(text,True,color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surf, text_rect)


class KingTower(pg.sprite.Sprite):
    def __init__(self, game, x, y, group, targetGroup):
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
        self.targetGroup = targetGroup
        self.target = None
        self.targetInRange = False
        self.timeSince = 0

    def findTarget(self):
        if len(self.targetGroup) > 0:
            troops = []
            troopDist = []
            # add distance from all troops to a list
            for troop in self.targetGroup:
                dist = math.sqrt((self.pos.x - troop.pos.x) ** 2 + (self.pos.y - troop.pos.y) ** 2)
                troops.append(troop)
                troopDist.append(dist)
            # set minimum distance
            minDist = troopDist.index(min(troopDist))
            # set target to closest troop
            self.target = troops[minDist]
            # check if target is close enough to shoot
            targetDist = math.sqrt((self.target.pos.x - self.pos.x) ** 2 + (self.target.pos.y - self.pos.y) ** 2)
            if targetDist < 175:
                self.targetInRange = True
            else:
                self.targetInRange = False
        else:
            self.target = None
            self.targetInRange = False

    def shoot(self):
        Arrow(self.game, self.pos.x, self.pos.y, self.game.arrows, self.target, self.targetGroup)
    def draw_health(self, screen):
        if self.hp > KING_HP * .6:
            color = GREEN
        elif self.hp > KING_HP * .3:
            color = YELLOW
        else:
            color = RED
        #set width of health bar and draw it
        width = self.rect.width / 2
        self.health_bar = pg.Rect(18.75,0,width,10)
        #draw bar
        pg.draw.rect(self.image, color, self.health_bar)
        draw_text(screen, str(self.hp), 10, BLACK, self.rect.x + (KING_SIZE / 2), self.rect.y - 2)

    def update(self):
        self.findTarget()
        if self.targetInRange and len(self.game.enemyTowers) < 3:
            self.timeSince += self.game.dt
            if self.timeSince > 1500:
                self.timeSince = 0
                self.shoot()
        # kill if hp runs out
        if self.hp <= 0:
            self.kill()

class ArcherTower(pg.sprite.Sprite):
    def __init__(self, game, x, y, group, targetGroup):
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((ARCHER_SIZE, ARCHER_SIZE))
        self.image.fill(BLUE)
        self.width = ARCHER_SIZE
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = (self.pos)
        self.hp = ARCHER_HP
        self.targetGroup = targetGroup
        self.target = None
        self.targetInRange = False
        self.timeSince = 0

    def findTarget(self):
        if len(self.targetGroup) > 0:
            troops = []
            troopDist = []
            #add distance from all troops to a list
            for troop in self.targetGroup:
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
                self.targetInRange = False
        else:
            self.target = None
            self.targetInRange = False

    def shoot(self):
        arrow = Arrow(self.game, self.pos.x, self.pos.y, self.game.arrows, self.target, self.targetGroup)

    def draw_health(self, screen):
        if self.hp > ARCHER_HP * .6:
            color = GREEN
        elif self.hp > ARCHER_HP * .3:
            color = YELLOW
        else:
            color = RED
        #set width of health bar and draw it
        width = self.rect.width / 2
        self.health_bar = pg.Rect(18.75,0,width,10)
        #draw bar
        pg.draw.rect(self.image, color, self.health_bar)
        draw_text(screen, str(self.hp), 10, BLACK, self.rect.x + (ARCHER_SIZE / 2), self.rect.y - 2)

    def update(self):
        self.findTarget()
        if self.targetInRange:
            self.timeSince += self.game.dt
            if self.timeSince > 1500:
                self.timeSince = 0
                self.shoot()
        #kill if hp runs out
        if self.hp <= 0:
            self.kill()

class Troop(pg.sprite.Sprite):
    def __init__(self, game, x, y, group, targetGroup):
        self.groups = game.all_sprites, group
        self.enemyTowers = game.enemyTowers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TROOP_SIZE, TROOP_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = (self.pos)

        self.hp = TROOP_HP
        self.damage = TROOP_DAMAGE
        self.targetGroup = targetGroup
        self.target = None
        self.timeSince = 0



    #calculate the distance between troop and towers and choose closest one
    def calcDistance(self):
        targets = []
        targetDist = []
        #go through every tower in the enemy towers group
        for tower in self.targetGroup:
            dist = math.sqrt((self.pos.x - tower.pos.x)**2 + (self.pos.y - tower.pos.y)**2)
            targetDist.append(dist) #append the distance from the tower to the tower distance list
            targets.append(tower) #append the tower to the towers list
        try:
            #find the index of closest tower in towers list
            minIndex = targetDist.index(min(targetDist))
            #set target to the minIndex from towers
            self.target = targets[minIndex]
        except:
            print('no')

    def avoid_troops(self):
        for troop in self.game.troops:
            if troop != self:
                dist = self.pos - troop.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.pos += dist.normalize()

    #attack target if colliding
    def attackTarget(self):
        hits = pg.sprite.spritecollide(self, self.targetGroup, False)
        if hits:
            self.target.hp -= self.damage
            print(self.target.hp)

    #draw health bar
    def draw_health(self, screen):
        if self.hp > TROOP_HP * .6:
            color = GREEN
        elif self.hp > TROOP_HP * .3:
            color = YELLOW
        else:
            color = RED
        #set width of health bar and draw it
        width = self.rect.width / 1.5
        self.health_bar = pg.Rect(5,0,width,5)
        #draw bar
        pg.draw.rect(self.image, color, self.health_bar)
        draw_text(screen, str(self.hp), 8, WHITE, self.rect.x + 12, self.rect.y - 10)

    def update(self):
        self.calcDistance()
        self.avoid_troops()
        # checks for collision with tower
        hits = pg.sprite.spritecollide(self, self.targetGroup, False)
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
    def __init__(self, game, x, y, group, target, targetGroup):
        self.groups = game.all_sprites, group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((10, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.center = (self.pos)
        self.target = target
        self.targetGroup = targetGroup

    def update(self):
        move(self, ARROW_SPEED)
        # check for collision with arrow
        hits = pg.sprite.spritecollide(self, self.targetGroup, True)
        if hits:
            self.target.hp -= ARROW_DAMAGE
            self.kill()

class CardTable(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((450,150))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x,y)
        self.rect.topleft = self.pos
        self.check1 = Card(self.game, x + 10, y + 15, self.game.cardChecks, BLUE, self)
        self.check2 = Card(self.game, x + 125, y + 15, self.game.cardChecks, BLUE, self)
        self.check3 = Card(self.game, x + 240, y + 15, self.game.cardChecks, BLUE, self)
        self.check4 = Card(self.game, x + 355, y + 15, self.game.cardChecks, BLUE, self)
        self.elixir = 10
        self.timer = 0

    def drawElixir(self, screen):
        draw_text(screen, "Elixir: " + str(self.elixir), 24, BLACK, self.pos.x + 45, self.pos.y - 35)
    def update(self):
        self.timer += self.game.dt
        if self.timer > 2000:
            if self.elixir < 10:
                self.elixir += 1
            self.timer = 0

class Card(pg.sprite.Sprite):
    def __init__(self, game, x, y, groups, color, cardTable):
        self.groups = game.all_sprites, groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((90, 125))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.topleft = self.pos
        self.color = color

        self.originalX = x
        self.originalY = y
        self.dragging = False
        self.spawn = False

    def update(self):
        pos = pg.mouse.get_pos()
        if self.dragging:
            self.image = pg.Surface((TROOP_SIZE, TROOP_SIZE))
            self.image.fill(BLACK)
            self.image.set_alpha(100)
            self.rect = self.image.get_rect()
            self.rect.centerx = pos[0]
            self.rect.centery = pos[1]
        else:
            self.image = pg.Surface((90, 125))
            self.image.fill(self.color)
            self.rect = self.image.get_rect()
            self.rect.topleft = (self.originalX, self.originalY)
            self.image.set_alpha(255)
        if self.spawn:
            self.kill()
            Troop(self.game, pos[0], pos[1], (self.game.troops, self.game.allPlayerSprites), self.game.enemies)

class Bound(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, groups):
        self.groups = game.all_sprites, groups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((w, h))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(x, y)
        self.rect.topleft = self.pos
        self.image.set_alpha(0)

