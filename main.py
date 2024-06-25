import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (179, 16, 16)     # 110, 110, 5


class Apple:
    """
    Represents the apple that the snake is going to eat.

    Attributes:
        image (pygame.Surface): Image of the apple.
        parent_screen (pygame.Surface): Screen on which the apple is drawn.
        x (int): x-coordinate of the apple.
        y (int): y-coordinate of the apple.
    """

    def __init__(self, parent_screen):
        """
        Initializes the apple with its image and initial position.

        Args:
            parent_screen (pygame.Surface): Screen on which the apple is drawn.
        """
        self.image = pygame.image.load("resources/apple3.png").convert()
        self.parent_screen = parent_screen
        self.x = 120
        self.y = 120

    def draw(self):
        """
        Drawing apple on the screen.
        """
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        """
        Moving apple to a random position on the screen.
        """
        self.x = random.randint(1, 25) * SIZE
        self.y = random.randint(1, 20) * SIZE


class Snake:
    """
    Represents the snake in the game.

    Attributes:
        parent_screen (pygame.Surface): Screen on which the snake is drawn.
        block (pygame.Surface): Image of a block of the snake.
        direction (str): Current direction of the movement of the snake.
        length (int): Length of the snake.
        x (list): x-coordinates of the snake blocks.
        y (list): y-coordinates of the snake blocks.
    """

    def __init__(self, parent_screen, length):
        """
        Initializing the snake with its length and initial position.

        Args:
            parent_screen (pygame.Surface): Screen on which the snake is drawn.
            length (int): Initial length of the snake.
        """
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'
        self.length = length
        self.x = [40] * length
        self.y = [40] * length

    def draw(self):
        """
        Drawing snake on the screen.
        """
        self.parent_screen.fill((8, 7, 7))   # 99, 99, 48 23, 117, 145
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    """Changing the snake's direction."""
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        """
        Moves the snake in the current direction.
        """
        # Body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # Head
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE

        # Wrap around screen edges
        self.x[0] %= 1200
        self.y[0] %= 900
        self.draw()

    def increase_length(self):
        """
        Increases the length of the snake by one block after eating each apple.
        """
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class CollisionException(Exception):
    """
    Custom exception to be raised when a collision occurs.
    """
    pass


class Game:
    """
    The main game logic.

    Attributes:
        surface (pygame.Surface): The game screen.
        snake (Snake): The snake in the game.
        apple (Apple): The apple in the game.
    """
    def __init__(self):
        """
        Initializes the game, including the snake and the apple.
        """
        pygame.init()
        pygame.display.set_caption("Snake and apple game project @ Ab-jr10")
        pygame.mixer.init()  # Initialize the mixer
        self.play_background_music()
        self.surface = pygame.display.set_mode((1200, 900))
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.font = pygame.font.SysFont('Arial', 30)

    def reset(self):
        """
        Resets the game by creating a new snake and apple.
        """
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)
        self.play_background_music()

    def collision(self, x1, y1, x2, y2):
        """
        Checks for a collision between two points.

        Args:
            x1 (int): x-coordinate of the first point.
            y1 (int): y-coordinate of the first point.
            x2 (int): x-coordinate of the second point.
            y2 (int): y-coordinate of the second point.

        Returns:
            bool: True if a collision is detected, False otherwise.
        """
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def scoring(self):
        """
        Displays the current score on the screen.
        """
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(score, (850, 10))

    def show_game_over(self):
        """
        Displays the game over screen.
        """
        self.render_background()
        font = pygame.font.SysFont('arial', 50)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def play(self):
        """
        Main game logic, including moving the snake, drawing the apple, and checking for collisions.
        """
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.scoring()
        pygame.display.flip()

        # eating apple
        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            self.play_sound('ding')

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise CollisionException("Game Over")

    def run(self):
        """
        Runs the game loop, handling events and updating the game state.
        """
        running = True
        pause = False
        sleep_time = 0.25

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
                    if self.snake.length % 5 == 0 and self.snake.length != 0:
                        sleep_time = max(0.1, sleep_time - 0.01)
            except CollisionException:
                self.show_game_over()
                pause = True
                self.reset()
                time.sleep(0.25) # Reset sleep time on game over

            time.sleep(sleep_time)

    def play_background_music(self):
        """
        Plays background music for the game.
        """
        # try:
        #     pygame.mixer.music.load('resources/bg_music_1.mp3')
        #     pygame.mixer.music.play(-1, 0)
        # except pygame.error as e:
        #     print(f"Error loading or playing background music: {e}")

        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1)

    def play_sound(self, sound_name):
        """
        Plays a sound effect.

        Args:
            sound_name (str): The name of the sound effect to play.
        """
        # try:
        #     if sound_name == "crash":
        #         sound = pygame.mixer.Sound("resources/crash.mp3")
        #     elif sound_name == 'ding':
        #         sound = pygame.mixer.Sound("resources/ding.mp3")
        #     pygame.mixer.Sound.play(sound)
        # except pygame.error as e:
        #     print(f"Error loading or playing sound: {e}")

        if sound_name == 'ding':
            sound = pygame.mixer.Sound('resources/ding.mp3')
        elif sound_name == 'crash':
            sound = pygame.mixer.Sound('resources/crash.mp3')
        pygame.mixer.Sound.play(sound)

    # def display_score(self):


if __name__ == "__main__":
    game = Game()
    game.run()

