#imports
from settings import *
from sprites import *
import pygame as pg

#YOU MUST INSTALL PYGAME ON YOUR COMPUTER FOR THIS GAME TO RUN

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.bg = pg.image.load(os.path.join(img_Folder, 'background-temp.png'))
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        #create sprite groups
        self.all_sprites = pg.sprite.Group()
        self.enemyTowers = pg.sprite.Group()
        self.enemyTroops = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.playerTowers = pg.sprite.Group()
        self.troops = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.cardChecks = pg.sprite.Group()
        self.cards = pg.sprite.Group()
        self.bounds = pg.sprite.Group()

        #create enemy towers
        self.enemyKing = KingTower(self, WIDTH / 2, 100, (self.enemyTowers, self.enemies), self.troops)
        self.enemyArcher1 = ArcherTower(self, WIDTH / 4, 155, (self.enemyTowers, self.enemies), self.troops)
        self.enemyArcher2 = ArcherTower(self, WIDTH * 3/4, 155, (self.enemyTowers, self.enemies), self.troops)
        #create enemy bounds
        self.kingBound = Bound(self, 0, 0, WIDTH, 200, (self.bounds))
        self.archerBound1 = Bound(self, 0, 200, WIDTH / 2, 150, (self.bounds))
        self.archerBound2 = Bound(self, WIDTH / 2, 200, WIDTH / 2, 150, (self.bounds))
        #enemy troop spawning funciton values
        self.enemyTimer = 0
        self.elixirTimer = 0
        self.enemyElixir = 10

        #create player towers
        self.playerKing = KingTower(self, WIDTH / 2, HEIGHT - 250, (self.playerTowers), self.enemyTroops)
        self.playerArcher1 = ArcherTower(self, WIDTH / 4, HEIGHT - 325, (self.playerTowers), self.enemyTroops)
        self.playerArcher2 = ArcherTower(self, WIDTH * 3/4, HEIGHT - 325, (self.playerTowers), self.enemyTroops)

        #create card table and cards
        self.cardTable = CardTable(self, 0, 650)

        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #spawn an enemy troop on a timer
        self.spawnEnemyTroop()
        #if cards list is less than 4 and card checks are not colliding with anything, spawn a card
        for check in self.cardChecks:
            hits = pg.sprite.spritecollide(check, self.cards, False)
            if not hits and len(self.cards) < 4:
                Card(self, check.rect.x, check.rect.y, (self.cards), YELLOW, self.cardTable)


        #Update loops
        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            #CHECK IF MOUSE IS CLICKED
            if event.type == pg.MOUSEBUTTONDOWN:
                #GET MOUES POSITION
                pos = pg.mouse.get_pos()
                for card in self.cards:
                    #IF THE MOUSE IS OVER THE CARD, SET DRAGGING TO TRUE
                    if card.rect.collidepoint(pos):
                        card.dragging = True
                #MAKE BOUNDS TRANSLUCENT
                for bound in self.bounds:
                    bound.image.set_alpha(100)
            #IF MOUSE BUTTON GOES UP
            if event.type == pg.MOUSEBUTTONUP:
                for card in self.cards:
                    #SET CARD DRAGGING TO FALSE
                    card.dragging = False
                    #IF CARD IS IN A SPAWNABLE ZONE, SPAWN TROOP
                    hits = pg.sprite.spritecollide(card, self.cardChecks, False)
                    inBounds = pg.sprite.spritecollide(card, self.bounds, False)
                    if not hits and not inBounds and self.cardTable.elixir >= 4:
                        card.spawn = True
                        self.cardTable.elixir -= 4
                for bound in self.bounds:
                    bound.image.set_alpha(0)

            #QUIT
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        #Draw sprites
        self.screen.blit(self.bg, (0,0))
        self.all_sprites.draw(self.screen)

        # draw health bars
        for sprite in self.all_sprites:
            if isinstance(sprite, ArcherTower):
                sprite.draw_health(self.screen)
            if isinstance(sprite, KingTower):
                sprite.draw_health(self.screen)
            if isinstance(sprite, Troop):
                sprite.draw_health(self.screen)
            if isinstance(sprite, CardTable):
                sprite.drawElixir(self.screen)


        #after drawing, flip display
        pg.display.flip()

    def spawnEnemyTroop(self):
        self.enemyTimer += self.dt
        self.elixirTimer += self.dt
        if self.enemyTimer > 2000:
            if self.enemyElixir < 10:
                self.enemyElixir += 1
                print(self.enemyElixir)
            if self.enemyElixir >= 4:
                Troop(self, random.randint(15, WIDTH - 15), 250, (self.enemies, self.enemyTroops), self.playerTowers)
                self.enemyElixir -= 4
                print("spawned")
            self.enemyTimer = 0

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()