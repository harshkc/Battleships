import os
import pygame

pygame.font.init()

# creates a window with defined width & height
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# sets window title
pygame.display.set_caption("BattleShips")

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# fonts
HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 80)

# game elements constant
FPS = 60
SPACESHIP_HEIGHT, SPACESHIP_WIDTH = 55, 40
VEL_SPACESHIP = 5
BULLET_WIDTH, BULLET_HEIGHT = 10, 5
VEL_BULLET = 12
MAX_BULLETS = 3

# user defined events
YELLOW_HITS = pygame.USEREVENT + 1
RED_HITS = pygame.USEREVENT + 2

# defines spaceships look and orientation
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


# we use spaceship height instead of width & vice-versa in movement
# as rect is rotated by 90 and 270 angle

def red_handle_movement(keys_pressed, red_rect):
    if keys_pressed[pygame.K_LEFT] and red_rect.x > WIDTH//2+5:
        red_rect.x -= VEL_SPACESHIP
    if keys_pressed[pygame.K_RIGHT] and red_rect.x < WIDTH - SPACESHIP_HEIGHT:
        red_rect.x += VEL_SPACESHIP
    if keys_pressed[pygame.K_UP] and red_rect.y > 0:
        red_rect.y -= VEL_SPACESHIP
    if keys_pressed[pygame.K_DOWN] and red_rect.y < HEIGHT-SPACESHIP_WIDTH:
        red_rect.y += VEL_SPACESHIP


def yellow_handle_movement(keys_pressed, yellow_rect):
    if keys_pressed[pygame.K_a] and yellow_rect.x > 0:
        yellow_rect.x -= VEL_SPACESHIP
    if keys_pressed[pygame.K_d] and yellow_rect.x < WIDTH//2 - (5+SPACESHIP_HEIGHT):
        yellow_rect.x += VEL_SPACESHIP
    if keys_pressed[pygame.K_w] and yellow_rect.y > 0:
        yellow_rect.y -= VEL_SPACESHIP
    if keys_pressed[pygame.K_s] and yellow_rect.y < HEIGHT-SPACESHIP_WIDTH:
        yellow_rect.y += VEL_SPACESHIP


def bullets_handling(bullets_yellow, bullets_red, yellow_rect, red_rect):
    for bullet in bullets_yellow:
        bullet.x += VEL_BULLET
        if red_rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HITS))
            bullets_yellow.remove(bullet)
        elif bullet.x > WIDTH:
            bullets_yellow.remove(bullet)

    for bullet in bullets_red:
        bullet.x -= VEL_BULLET
        if yellow_rect.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HITS))
            bullets_red.remove(bullet)
        elif bullet.x < 0:
            bullets_red.remove(bullet)


def draw_winner(winner_text):
    winner_text_style = WINNER_FONT.render(winner_text, 1, WHITE)
    WIN.blit(winner_text_style, (WIDTH//2-winner_text_style.get_width()//2,
             HEIGHT//2-winner_text_style.get_height()))
    pygame.display.update()
    pygame.time.delay(5000)


def draw_window(yellow_rect, red_rect, bullets_yellow, bullets_red, health_yellow, health_red):
    WIN.blit(SPACE_BG, (0, 0))
    pygame.draw.rect(WIN, BLACK, CENTRE_BORDER)

    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(health_yellow), 1, WHITE)
    red_health_text = HEALTH_FONT.render(
        "Health: " + str(health_red), 1, WHITE)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow_rect.x, yellow_rect.y))
    WIN.blit(RED_SPACESHIP, (red_rect.x, red_rect.y))

    for bullet in bullets_yellow:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in bullets_red:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def main():
    yellow_rect = pygame.Rect(
        100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_rect = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # keeps track of bullets and helps limiting bullets on the screen
    bullets_yellow = []
    bullets_red = []

    health_yellow = 10
    health_red = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            # handles bullets movement and fired position
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(bullets_yellow) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow_rect.x + SPACESHIP_HEIGHT,
                                         yellow_rect.y + SPACESHIP_WIDTH//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    bullets_yellow.append(bullet)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(bullets_red) < MAX_BULLETS:
                    bullet = pygame.Rect(red_rect.x,
                                         red_rect.y + SPACESHIP_WIDTH//2 - 2, BULLET_WIDTH, BULLET_HEIGHT)
                    bullets_red.append(bullet)

            if event.type == RED_HITS:
                health_yellow -= 1

            if event.type == YELLOW_HITS:
                health_red -= 1

        winner_text = ""
        if health_yellow <= 0:
            winner_text += "Team Defender Won!!!"
        if health_red <= 0:
            winner_text += "Team Galatic Won!!!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        # spaceship movement handling
        keys_pressed_list = pygame.key.get_pressed()
        red_handle_movement(keys_pressed_list, red_rect)
        yellow_handle_movement(keys_pressed_list, yellow_rect)

        # handles bullet movement and collision handling
        bullets_handling(bullets_yellow, bullets_red, yellow_rect, red_rect)

        # drawing UI elements
        draw_window(yellow_rect, red_rect, bullets_yellow,
                    bullets_red, health_yellow, health_red)

    main()


if __name__ == "__main__":
    main()
