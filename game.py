import pygame
import tmx

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image = pygame.image.load('player.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.resting = False
        self.dy = 0

    def get_x_position(self):
        return self.rect.x

    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt

        if self.resting and key[pygame.K_SPACE]:
            self.dy = -300
        self.dy = min(200, self.dy + 40)

        self.rect.y += self.dy * dt

        new = self.rect
        #print(new)
        self.resting = False
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0
        #print(new.x, new.y)
        game.tilemap.set_focus(new.x, new.y)

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
            new_x = self.player.get_x_position()
            if new_x < w-900:
                if last_x != new_x:
                    if last_x < new_x:
                        x -= (last_x + (new_x/32.)) / 100.
                    else:
                        x += (last_x + (new_x/32.)) / 100.
                    last_x = new_x
            else:
                x = -821

            self.tilemap.update(dt / 1000., self)
            screen.blit(background, (x, 0))

            self.tilemap.draw(screen)
            pygame.display.flip()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    Game().main(screen)

