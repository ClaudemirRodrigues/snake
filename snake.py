import pygame, random
from pygame.locals import *
import pygame.mixer
from time import sleep


def on_grid_random():
    x = random.randint(0, 590)
    y = random.randint(0, 590)
    return x // 10 * 10, y // 10 * 10


def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])


UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Cobrinha do Bill!')

snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((150, 150, 150))

apple_pos = on_grid_random()
apple = pygame.Surface((10, 10))
apple.fill((80, 220, 80))

my_direction = LEFT

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 18)
score = 0

game_over = False

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(0)

efeito = pygame.mixer.Sound('efeito.wav')
batida = pygame.mixer.Sound('explosion.wav')
speed = 5

while not game_over:

    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_UP:
                my_direction = UP
            if event.key == K_DOWN:
                my_direction = DOWN
            if event.key == K_LEFT:
                my_direction = LEFT
            if event.key == K_RIGHT:
                my_direction = RIGHT

    # detectar quando pega o ponto
    if collision(snake[0], apple_pos):
        efeito.play(0)
        apple_pos = on_grid_random()
        snake.append((0, 0))
        score = score + 1
        speed += .2

    # detectar colisões nas paredes
    if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
        batida.play(0)
        print(f'Você marcou {score} pontos.')
        sleep(2)
        game_over = True
        break

    # detectar colisão com ela mesma
    for i in range(1, len(snake) - 1):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
            batida.play(0)
            print(f'Você marcou {score} pontos.')
            sleep(2)
            game_over = True
            break

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i - 1][0], snake[i - 1][1])

    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - 10)
    if my_direction == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + 10)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + 10, snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - 10, snake[0][1])

    screen.fill((0, 0, 0))
    screen.blit(apple, apple_pos)

    # desenha a grade
    for x in range(0, 600, 10):
        pygame.draw.line(screen, (3, 3, 3), (x, 0), (x, 600))
    for y in range(0, 600, 10):
        pygame.draw.line(screen, (3, 3, 3), (0, y), (600, y))

    # marcador de pontos
    score_font = font.render('Pontos: %s' % (score), True, (255, 255, 255))
    score_rect = score_font.get_rect()
    score_rect.topleft = (600 - 120, 10)
    screen.blit(score_font, score_rect)

    for pos in snake:
        screen.blit(snake_skin, pos)

    pygame.display.update()
    
