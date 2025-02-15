import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
FPS = 60
GRAVITY = 0.6
JUMP_FORCE = -12
OBSTACLE_SPEED = 7

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game")
clock = pygame.time.Clock()

class Dino:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.x = 50
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
        self.vel_y = 0
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.vel_y = JUMP_FORCE
            self.jumping = True

    def update(self):
        self.vel_y += GRAVITY
        self.y += self.vel_y
        
        if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.jumping = False
            self.vel_y = 0

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height))

class Cactus:
    def __init__(self):
        self.width = 30
        self.height = 50
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height

    def update(self):
        self.x -= OBSTACLE_SPEED

    def draw(self):
        pygame.draw.rect(screen, GREY, (self.x, self.y, self.width, self.height))

def main():
    dino = Dino()
    obstacles = []
    spawn_timer = 0
    score = 0
    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_over:
                        main()  # Restart game
                    else:
                        dino.jump()
                elif event.key == pygame.K_UP:
                    dino.change_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    dino.change_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    dino.change_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    dino.change_direction(1, 0)

        if not game_over:
            # Spawn obstacles
            spawn_timer += 1
            if spawn_timer > random.randint(40, 100):
                obstacles.append(Cactus())
                spawn_timer = 0

            # Update game elements
            dino.update()
            for obstacle in obstacles:
                obstacle.update()

            # Remove off-screen obstacles
            obstacles = [obstacle for obstacle in obstacles if obstacle.x > -obstacle.width]

            # Collision detection
            dino_rect = pygame.Rect(dino.x, dino.y, dino.width, dino.height)
            for obstacle in obstacles:
                obstacle_rect = pygame.Rect(obstacle.x, obstacle.y, obstacle.width, obstacle.height)
                if dino_rect.colliderect(obstacle_rect):
                    game_over = True

            # Update score
            score += 1

        # Draw everything
        screen.fill(BLACK)
        pygame.draw.rect(screen, GREY, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        dino.draw()
        for obstacle in obstacles:
            obstacle.draw()

        # Draw score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score//10}", True, WHITE)
        screen.blit(text, (10, 10))

        if game_over:
            text = font.render("Game Over! Press SPACE to restart", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2))

        pygame.display.flip()
        clock.tick(FPS)

        if not running:
            pygame.quit()
            return

if __name__ == "__main__":
    main()