import pygame
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600


class Player(pygame.sprite.Sprite):
    def __init__(self, x_coord=0, image_location='', is_player_two=False):
        super(Player, self).__init__()
        self.is_player_two = is_player_two
        self.image = pygame.image.load(image_location).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x_coord
        self.rect.y = 500

    def update(self) -> None:
        key = pygame.key.get_pressed()
        if self.is_player_two:
            if key[pygame.K_UP]:
                self.rect.y -= 3
            if key[pygame.K_DOWN] and self.rect.y <= 500:
                self.rect.y += 3
            return

        if key[pygame.K_w]:
            self.rect.y -= 3
        if key[pygame.K_s] and self.rect.y <= 500:
            self.rect.y += 3


class Meteor(pygame.sprite.Sprite):
    def __init__(self, is_right_movement=False):
        super(Meteor, self).__init__()
        self.image = pygame.image.load('resources/images/meteor_small.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.is_right_movement = is_right_movement

    def update(self):
        if self.is_right_movement:
            self.rect.x += 1
            if self.rect.x >= 900:
                self.rect.x = 0

        else:
            self.rect.x -= 1
            if self.rect.x < 0:
                self.rect.x = 910

        if self.rect.x < 0 or self.rect.x > 900:
            self.rect.y = random.randrange(42, 450)


class Star(pygame.sprite.Sprite):
    def __init__(self, is_star_two=False):
        super(Star, self).__init__()
        self.image = pygame.image.load('./resources/images/star_silver.png').convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = 20

        if not is_star_two:
            self.rect.x = (SCREEN_WIDTH // 2) - 166
        else:
            self.rect.x = (SCREEN_WIDTH // 2) + 134


class Game:
    def __init__(self):
        self.player1_score = 0
        self.player2_score = 0
        self.game_over = False
        self.my_font = pygame.font.SysFont('Liberation Mono', 24)
        self.player1_counter = self.my_font.render(
            f'Player 1: {self.player1_score}', False, WHITE
        )
        self.player2_counter = self.my_font.render(
            f'Player 2: {self.player2_score}', False, WHITE
        )

        self.meteor_list = pygame.sprite.Group()
        self.star_list = pygame.sprite.Group()
        self.star_list2 = pygame.sprite.Group()
        self.all_sprite_list = pygame.sprite.Group()

        for i in range(10):
            meteor = Meteor()
            right_meteor = Meteor(True)
            meteor.rect.x = random.randrange(900)
            meteor.rect.y = random.randrange(42, 460)
            right_meteor.rect.x = random.randrange(900)
            right_meteor.rect.y = random.randrange(42, 460)

            self.meteor_list.add(meteor)
            self.all_sprite_list.add(meteor)

            self.meteor_list.add(right_meteor)
            self.all_sprite_list.add(right_meteor)

        self.player1 = Player((SCREEN_WIDTH // 2) - 200, './resources/images/player01.png')
        self.player2 = Player((SCREEN_WIDTH // 2) + 100, './resources/images/player02.png', True)

        self.star = Star()
        self.star2 = Star(True)

        self.star_list.add(self.star)
        self.star_list2.add(self.star2)

        self.all_sprite_list.add(self.player1)
        self.all_sprite_list.add(self.player2)

        self.all_sprite_list.add(self.star)
        self.all_sprite_list.add(self.star2)

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False

    def run_logic(self):
        self.all_sprite_list.update()

        # add collisions
        if pygame.sprite.spritecollide(self.player1, self.star_list, False):
            self.player1_score += 1
            self.player1_counter = self.my_font.render(
                f'Player 1: {self.player1_score}', False, WHITE
            )
            self.player1.rect.y = 500

            print(self.player1_score)

        if pygame.sprite.spritecollide(self.player2, self.star_list2, False):
            self.player2_score += 1
            self.player2_counter = self.my_font.render(
                f'Player 2: {self.player2_score}', False, WHITE
            )
            self.player2.rect.y = 500

            print(self.player2_score)

        if pygame.sprite.spritecollide(self.player1, self.meteor_list, False):
            self.player1.rect.y = 500

        if pygame.sprite.spritecollide(self.player2, self.meteor_list, False):
            self.player2.rect.y = 500

    def display_frame(self, screen, background):
        # screen.fill(BLACK)
        screen.blit(background, [0, 0])

        screen.blit(self.player1_counter, (56, 5))
        screen.blit(self.player2_counter, ((SCREEN_WIDTH - 200), 5))

        if not self.game_over:
            self.all_sprite_list.draw(screen)
        pygame.display.flip()


def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = pygame.image.load('./resources/images/background2-min.jpg')
    pygame.display.set_caption('Space Race')
    icon = pygame.image.load('./resources/images/player01.png')
    pygame.display.set_icon(icon)
    done = False
    clock = pygame.time.Clock()

    game = Game()

    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen, background)
        clock.tick(60)

    pygame.font.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
