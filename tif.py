#!/usr/bin/python
 
import pygame
import sys
from game import Game

 
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
DARK_BLUE = (35, 38, 56)
BABY_BLUE = (94, 119, 163)
DARK_GREEN = (103, 163, 131)

class MenuItem(pygame.font.Font):
    def __init__(self, text, font=None, font_size=30,
                 font_color=DARK_GREEN, (pos_x, pos_y)=(0, 0)):
        pygame.font.Font.__init__(self, font, font_size)
        self.text = text
        self.font_size = font_size
        self.font_color = font_color
        self.label = self.render(self.text, 1, self.font_color)
        self.width = self.label.get_rect().width
        self.height = self.label.get_rect().height
        self.dimensions = (self.width, self.height)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.position = pos_x, pos_y
        self.is_selected = False
 
    def set_position(self, x, y):
        self.position = (x, y)
        self.pos_x = x
        self.pos_y = y
 
    def set_font_color(self, rgb_tuple):
        self.font_color = rgb_tuple
        self.label = self.render(self.text, 1, self.font_color)
 
    def is_mouse_selection(self, (posx, posy)):
        if (posx >= self.pos_x and posx <= self.pos_x + self.width) and \
            (posy >= self.pos_y and posy <= self.pos_y + self.height):
                return True
        return False
 
 
class GameMenu():
    def __init__(self, screen, items, funcs, bg_color=DARK_BLUE, font=None, font_size=30,
                    font_color=DARK_GREEN):
        self.screen = screen
        self.scr_width = self.screen.get_rect().width
        self.scr_height = self.screen.get_rect().height
 
        self.bg_color = bg_color
        self.clock = pygame.time.Clock()
 
        self.items = []
        for index, item in enumerate(items):
            menu_item = MenuItem(item, font, font_size, font_color)
 
            # t_h: total height of text block
            t_h = len(items) * menu_item.height
            pos_x = (self.scr_width / 2) - (menu_item.width / 2)
            pos_y = (self.scr_height / 2) - (t_h / 2) + ((index*2) + index * menu_item.height)
 
            menu_item.set_position(pos_x, pos_y)
            self.items.append(menu_item)
 
        self.mouse_is_visible = True
        self.cur_item = None
        self.funcs = funcs
 
    def set_mouse_visibility(self):
        if self.mouse_is_visible:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
 
    def set_item_selection(self, key):
        """
        Marks the MenuItem chosen via up and down keys.
        """
        for item in self.items:
            # Return all to neutral
            item.set_font_color(DARK_GREEN)
 
        if self.cur_item is None:
            self.cur_item = 0
        else:
            # Find the chosen item
            if key == pygame.K_UP and self.cur_item > 0:
                self.cur_item -= 1
            elif key == pygame.K_UP and self.cur_item == 0:
                self.cur_item = len(self.items) - 1
            elif key == pygame.K_DOWN and self.cur_item < len(self.items) - 1:
                self.cur_item += 1
            elif key == pygame.K_DOWN and self.cur_item == len(self.items) - 1:
                self.cur_item = 0
 
        self.items[self.cur_item].set_font_color(BABY_BLUE)

        if key == pygame.K_SPACE or key == pygame.K_RETURN:
            text = self.items[self.cur_item].text
            self.funcs[text]()
 
    def set_mouse_selection(self, item, mpos):
        """Marks the MenuItem the mouse cursor hovers on."""
        if item.is_mouse_selection(mpos):
            item.set_font_color(BABY_BLUE)
        else:
            item.set_font_color(DARK_GREEN)

    def run(self):
        mainloop = True
        while mainloop:
            # Limit frame speed to 50 FPS
            self.clock.tick(50)
            mpos = pygame.mouse.get_pos()
 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                    sys.exit
                if event.type == pygame.KEYDOWN:
                    self.mouse_is_visible = False
                    self.set_item_selection(event.key)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.is_mouse_selection(mpos):
                            self.funcs[item.text]()
 
            if pygame.mouse.get_rel() != (0, 0):
                self.mouse_is_visible = True
                self.cur_item = None
 
            self.set_mouse_visibility()
 
            # Redraw the background
            self.screen.fill(self.bg_color)
 
            for item in self.items:
                if self.mouse_is_visible:
                    mpos = pygame.mouse.get_pos()
                    self.set_mouse_selection(item, mpos)
                self.screen.blit(item.label, item.position)
 
            pygame.display.flip()
 

def display_settings():
    settings_funcs = {'Use the arrows to move around. Use space to jump '
                      'and left shift to shoot some amazing facts.': display_settings,
                      'Return': load_main_menu}
    pygame.display.set_caption('Settings Menu')
    settings_menu = GameMenu(screen, settings_funcs.keys(), settings_funcs)
    settings_menu.run()


def start_game():
    Game(screen).main()


def load_main_menu():
    funcs = {'Start': start_game,
             'Settings': display_settings,
             'Quit': sys.exit}

    pygame.display.set_caption('Game Menu')
    gm = GameMenu(screen, funcs.keys(), funcs)
    gm.run()

if __name__ == "__main__":
    pygame.init()
    
    # Creating the screen
    screen = pygame.display.set_mode((1280, 720), 0, 32)
    load_main_menu()



