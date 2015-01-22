import pygame

class Enemy(pygame.sprite.Sprite):

    def __init__(self, location, *groups):
        super(Enemy, self).__init__(*groups)
        self.direction = 1
        self.image_left = pygame.image.load('resources/characters/enemy1_izquierda.png')
        self.image_right = pygame.image.load('resources/characters/enemy1_derecha.png')
        self.image = self.image_left
        self.rect = pygame.rect.Rect(location, self.image.get_size())


    def update(self, dt, game):
        self.rect.x += self.direction * 100 * dt
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            if self.direction > 0:
                self.rect.right = cell.left
                self.image = self.image_left
            else:
                self.rect.left = cell.right
                self.image = self.image_right
            self.direction *= -1
            break
        if self.rect.colliderect(game.player.rect):
            game.player.is_dead = True