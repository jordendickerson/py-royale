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
        #create enemy towers
        self.enemyKing = KingTower(self, WIDTH / 2, 100, (self.all_sprites, self.enemyTowers))
        self.enemyArcher1 = ArcherTower(self, WIDTH / 4, 155, (self.all_sprites, self.enemyTowers))
        self.enemyArcher2 = ArcherTower(self, WIDTH * 3/4, 155, (self.all_sprites, self.enemyTowers))
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #Update loops
        self.all_sprites.update()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        #Draw sprites
        self.screen.blit(self.bg, (0,0))
        self.all_sprites.draw(self.screen)

        #after drawing, flip display
        pg.display.flip()

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