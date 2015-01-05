import pygame
from libs import tmx
from player import Player

class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        # Load the background and get its properties
        background = pygame.image.load('resources/backgrounds/mountains.png')
        background_size = background.get_size()
        x = 0
        w, h = background_size

        self.tilemap = tmx.load("resources/maps/map.tmx", screen.get_size())

        self.sprites = tmx.SpriteLayer()

        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player((start_cell.px, start_cell.py), self.sprites)
        last_x = self.player.get_x_position()
        self.tilemap.layers.append(self.sprites)

        while 1:
            dt = clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            self.tilemap.update(dt / 1000., self)
            screen.blit(background, ((-self.tilemap.viewport.x/2), 0))

            self.tilemap.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    Game().main(screen)

