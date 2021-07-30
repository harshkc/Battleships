import os
import pygame

# creates a window with defined width & height
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# set window title
pygame.display.set_caption("BattleShips")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
red_coordinates = (255, 0, 0)
yellow_coordinates = (255, 255, 0)

# TODO: bullets firing, collision handling, health deprecation, winner text

# game elements constant
FPS = 60
SPACESHIP_HEIGHT, SPACESHIP_WIDTH = 55, 40
VEL_SPACESHIP = 5

# defining spaceships look and orientation
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE_BG = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

CENTRE_BORDER = pygame.Rect(WIDTH//2-5, 0, 10, HEIGHT)


def red_handle_movement(keys_pressed, red_coordinates):
    if keys_pressed[pygame.K_LEFT] and red_coordinates.x > WIDTH//2+5:
        red_coordinates.x -= VEL_SPACESHIP
    if keys_pressed[pygame.K_RIGHT] and red_coordinates.x < WIDTH - SPACESHIP_HEIGHT:
        red_coordinates.x += VEL_SPACESHIP
    if keys_pressed[pygame.K_UP] and red_coordinates.y > 0:
        red_coordinates.y -= VEL_SPACESHIP
    if keys_pressed[pygame.K_DOWN] and red_coordinates.y < HEIGHT-SPACESHIP_WIDTH:
        red_coordinates.y += VEL_SPACESHIP


def yellow_handle_movement(keys_pressed, yellow_coordinates):
    if keys_pressed[pygame.K_a] and yellow_coordinates.x > 0:
        yellow_coordinates.x -= VEL_SPACESHIP
    if keys_pressed[pygame.K_d] and yellow_coordinates.x < WIDTH//2 - (5+SPACESHIP_HEIGHT):
        yellow_coordinates.x += VEL_SPACESHIP
    if keys_pressed[pygame.K_w] and yellow_coordinates.y > 0:
        yellow_coordinates.y -= VEL_SPACESHIP
    if keys_pressed[pygame.K_s] and yellow_coordinates.y < HEIGHT-SPACESHIP_WIDTH:
        yellow_coordinates.y += VEL_SPACESHIP


def draw_window(yellow_coordinates, red_coordinates):
    WIN.blit(SPACE_BG, (0, 0))
    pygame.draw.rect(WIN, BLACK, CENTRE_BORDER)

    WIN.blit(YELLOW_SPACESHIP, (yellow_coordinates.x, yellow_coordinates.y))
    WIN.blit(RED_SPACESHIP, (red_coordinates.x, red_coordinates.y))
    pygame.display.update()


def main():
    yellow_coordinates = pygame.Rect(
        100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_coordinates = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        # spaceship movement handling
        keys_pressed_list = pygame.key.get_pressed()
        red_handle_movement(keys_pressed_list, red_coordinates)
        yellow_handle_movement(keys_pressed_list, yellow_coordinates)

        # drawing UI elements
        draw_window(yellow_coordinates, red_coordinates)

    main()


if __name__ == "__main__":
    main()
