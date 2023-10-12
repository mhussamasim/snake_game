import pygame
from pygame.locals import *  # imports certain global variables
import random
import time

width = 1072
height = 720
background_color = (0, 0, 0)
text_color = (255, 255, 255)
size = 16  # no. of pixels per snake and apple block
render_time = 0.2


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length

        self.block = pygame.image.load("resources/block.jpg").convert()  # loads image
        self.x = [size] * length
        self.y = [size] * length
        self.direction = "down"  # direction the snake is moving

    def draw(self):
        self.parent_screen.fill(background_color)
        for i in range(0, self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))  # renders blocks to snake length

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "up":
            self.y[0] -= size
        if self.direction == "down":
            self.y[0] += size
        if self.direction == "left":
            self.x[0] -= size
        if self.direction == "right":
            self.x[0] += size

        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen

        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = 64
        self.y = 64

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))

    def move(self):
        self.x = random.randint(0, int(width / size) - 1) * size
        self.y = random.randint(0, int(height / size) - 1) * size


class Game:
    def __init__(self):
        pygame.init()  # .init method initializes all PyGame modules
        self.surface = pygame.display.set_mode((width, height))  # set_mode initializes the game window - see constants
        self.surface.fill(background_color)  # fills the background with color - rgb
        self.snake = Snake(self.surface, 3)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.render_time = render_time

    @staticmethod
    def is_collision(x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return True
        return False

    def collision_snake(self):
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"

    def collision_apple(self):
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.apple.move()
            self.snake.increase_length()
            self.render_time -= 0.005

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)  # selects the font and font size
        player_score = font.render(f"Score: {self.snake.length - 3}", True, text_color)
        self.surface.blit(player_score, (0, 0))

    def game_over(self):
        self.surface.fill(background_color)
        font = pygame.font.SysFont("arial", 30)
        game_over_message = font.render(f"Game Over! Your Score: {self.snake.length - 3}", True, text_color)
        self.surface.blit(game_over_message, ((width / 2) - 144, (height / 2) - 32))
        try_again_message = font.render("Play again (Enter)? Quit (Esc)?", True, text_color)
        self.surface.blit(try_again_message, ((width / 2) - 160, (height / 2) + 16))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 3)
        self.apple = Apple(self.surface)
        self.render_time = 0.2

    def render(self):
        self.snake.walk()
        self.apple.draw()
        self.collision_apple()
        self.collision_snake()
        self.display_score()
        pygame.display.flip()

    def run(self):
        self.render()

        running = True
        pause = False

        while running:
            for event in pygame.event.get():  # .event.get returns all events that can be processed
                if event.type == KEYDOWN:  # KEYDOWN came from pygame.locals
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pause = False
                    if event.key == K_UP:
                        self.snake.move_up()
                    if event.key == K_DOWN:
                        self.snake.move_down()
                    if event.key == K_LEFT:
                        self.snake.move_left()
                    if event.key == K_RIGHT:
                        self.snake.move_right()

                elif event.type == QUIT:  # QUIT is the X button at the corner of a window
                    running = False
            try:
                if not pause:
                    self.render()
            except Exception:
                self.game_over()
                pause = True
                self.reset()

            time.sleep(self.render_time)  # Suspends for loop execution for 0.2 seconds


if __name__ == "__main__":
    game = Game()
    game.run()
