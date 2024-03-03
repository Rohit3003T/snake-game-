import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, text_color, bg_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bg_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.score = 0

    def move(self):
        current_head = self.body[0]
        new_head = (current_head[0] + self.direction[0], current_head[1] + self.direction[1])
        # Check for boundary conditions
        if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
            return False  # Snake hit the wall
        self.body.insert(0, new_head)
        self.body.pop()
        return True

    def grow(self):
        current_head = self.body[0]
        new_head = (current_head[0] + self.direction[0], current_head[1] + self.direction[1])
        self.body.insert(0, new_head)
        self.score += 1

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Food class
class Food:
    def __init__(self):
        self.position = self.randomize_position()

    def randomize_position(self):
        return random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Game Over screen
def game_over():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 72)
    text_surface = font.render("Game Over", True, WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Main function
def main():
    clock = pygame.time.Clock()

    start_button = Button(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100, "Start Game", WHITE, GREEN)
    snake = None
    food = None
    font = pygame.font.Font(None, 36)
    game_started = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started and start_button.is_clicked(event.pos):
                    snake = Snake()
                    food = Food()
                    game_started = True
            elif event.type == pygame.KEYDOWN:
                if game_started:
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)

        screen.fill(BLACK)

        if game_started:
            snake_move_result = snake.move()
            if not snake_move_result:
                # If snake hits the wall, show game over screen
                game_over()
                game_started = False

            if snake.body[0] == food.position:
                snake.grow()
                food.position = food.randomize_position()

            snake.draw()
            food.draw()

            text = font.render(f"Score: {snake.score}", True, WHITE)
            screen.blit(text, (10, 10))
        else:
            start_button.draw(screen)

        pygame.display.flip()

        clock.tick(10)  # Adjust snake speed

    pygame.quit()

if __name__ == "__main__":
    main()
