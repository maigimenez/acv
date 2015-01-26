import pygame
from libs import tmx
from player import Player
from enemy import Enemy

class Game(object):
    def __init__(self, screen):
        # Load the background and get its properties
        self.background = pygame.image.load('resources/backgrounds/mountains.png')
        self.background_size = self.background.get_size()

        self.screen = screen
        self.tile_map = tmx.load("resources/maps/map.tmx", self.screen.get_size())
        self.sprites = tmx.SpriteLayer()
        self.enemies = tmx.SpriteLayer()

        # Load the player
        start_cell = self.tile_map.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)

        # Load the enemies
        for enemy in self.tile_map.layers['triggers'].find('enemy'):
            Enemy((enemy.px, enemy.py), self.enemies)
        self.tile_map.layers.append(self.enemies)

    def main(self):
        # System clock to synchronize
        clock = pygame.time.Clock()

        # Variables to handle the scroll
        x = 0
        w, h = self.background_size

        last_x = self.player.get_x_position()
        self.tile_map.layers.append(self.sprites)

        # Main loop
        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.tile_map.update(dt / 1000., self)
            self.screen.blit(self.background,
                        ((-self.tile_map.viewport.x/2), 0))

            self.tile_map.draw(self.screen)
            pygame.display.flip()

            if self.player.is_dead:
                print ("Has muerto!")
                return

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    Game(screen).main()

