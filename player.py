import pygame
from weapon import Weapon

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        self.image_right = pygame.image.load('resources/characters/nena_derecha.png')
        self.image_left = pygame.image.load('resources/characters/nena_izquierda.png')
        self.image = self.image_right
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        self.resting = False
        self.dy = 0
        self.is_dead = False
        self.direction = 1
        self.cool_down = 0

    def get_x_position(self):
        return self.rect.x

    def update(self, dt, game):
        last = self.rect.copy()

        key = pygame.key.get_pressed()
        # Handle a step to the left
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
            self.image = self.image_left
            self.direction = -1

        # Handle a step to the right
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
            self.image = self.image_right
            self.direction = 1

        # Handle a shoot
        if key[pygame.K_LSHIFT] and not self.cool_down:
            if self.direction > 0:
                Weapon(self.rect.midright, 1, game.sprites)
            else:
                Weapon(self.rect.midleft, -1, game.sprites)
            self.cool_down = 1
        self.cool_down = max(0, self.cool_down - dt)

        # Handle a jump
        if self.resting and key[pygame.K_SPACE]:
            self.dy = -600
        self.dy = min(300, self.dy + 40)

        self.rect.y += self.dy * dt

        new = self.rect
        self.resting = False
        for cell in game.tile_map.layers['triggers'].collide(new, 'blockers'):
            blockers = cell['blockers']
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if  't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
                self.dy = 0
            if  'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
                self.dy = 0
        game.tile_map.set_focus(new.x, new.y)