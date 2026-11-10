
import random
import pygame


# Game settings

# Screen
WIDTH, HEIGHT = 800, 600
FPS = 60

# Paddle
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 15
PADDLE_SPEED = 7

# Ball
BALL_SIZE = 15
BALL_SPEED = 5


# Parent class for all game entities
class Entity:
    # Initializes an instance of the entity
    def __init__(self, center, width, height):
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center
        self.velocity = pygame.Vector2()

    # Determines the behaviour of the entity each frame
    def update(self):
        self.rect.move_ip(self.velocity)

    # Checks whether this entity collides with another entity
    def collides(self, other):
        return self.rect.colliderect(other.rect)


# Paddle class that inherits from Entity
class Paddle(Entity):
    # Initializes an instance of the paddle
    def __init__(self, center, width, height, speed):
        super().__init__(center, width, height)
        self.speed = speed

    # Updates the paddle's position and velocity
    def update(self, direction, bounds):
        self.velocity.x = direction * self.speed
        super().update()
        self.rect.clamp_ip(bounds)


# Ball class that inherits from Entity
class Ball(Entity):
    # Initializes an instance of the ball
    def __init__(self, size, speed, center):
        super().__init__(center, size, size)
        self.speed = speed
        self.center = center
        self.reset()

    # Resets the ball to the center of the screen and gives it a random velocity
    def reset(self):
        self.rect.center = self.center
        self.velocity.update(
            random.choice([-self.speed, self.speed]),
            random.choice([-self.speed, self.speed])
        )

    # Bounces the ball off another entity
    def bounce(self, entity):
        # Prevents multiple collisions by moving the ball out of the entitys hitbox.
        if self.velocity.y > 0:
            self.rect.bottom = entity.rect.top
        else:
            self.rect.top = entity.rect.bottom

        self.velocity.y *= -1

    # Updates the ball's movement and handles collisions
    def update(self, entities, bounds):
        super().update()

        # Bounce off side walls
        if self.rect.left <= bounds.left or self.rect.right >= bounds.right:
            self.velocity.x *= -1
            self.rect.clamp_ip(bounds)

        # Bounce off other entities
        for entity in entities:
            if self.collides(entity):
                self.bounce(entity)
                # Exits codes early and returns True to indicate a collision occurred
                return True

        # Reset when a player misses
        if not bounds.colliderect(self.rect):
            self.reset()

        # Returns False to indicate no collision occurred
        return False


class Game:
    # Initializes an instance of the game
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Two Player Pong")
        self.clock = pygame.time.Clock()
        self.bounds = self.screen.get_rect()


        self.paddles = [
            Paddle(
                (self.bounds.centerx, 40),
                PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED
            ),
            Paddle(
                (self.bounds.centerx, self.bounds.bottom - 55),
                PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED
            )
        ]

        self.ball = Ball(BALL_SIZE, BALL_SPEED, self.bounds.center)
        self.hit_sound = pygame.mixer.Sound("hit.ogg")
        self.running = True

    # Updates the game state
    def update(self):
        keys = pygame.key.get_pressed()

        # Input bindings
        directions = [
            # Player 1 Input keys
            int(keys[pygame.K_d]) - int(keys[pygame.K_a]),
            # Player 2 Input keys
            int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        ]

        for paddle, direction in zip(self.paddles, directions):
            paddle.update(direction, self.bounds)

        if self.ball.update(self.paddles, self.bounds):
            self.hit_sound.play()

    # Draws the graphics of the game
    def draw(self):
        self.screen.fill("black")

        for entity in [*self.paddles, self.ball]:
            pygame.draw.rect(self.screen, "white", entity.rect)

        pygame.display.flip()

    # Where the game loop is run and events are handled
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.draw()
            # Framerate the game loops in.
            self.clock.tick(FPS)

        pygame.quit()

# Runs the game if this file is executed directly 
if __name__ == "__main__":
    Game().run()
