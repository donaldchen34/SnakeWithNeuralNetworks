import pygame
from math import floor
import random
from datetime import datetime
from collections import deque

#Global Settings
GridSize = 15 #15x15
Grid = [[0 for i in range(GridSize)] for j in range(GridSize)]
SCREEN_SIZE = 600,600
screen = pygame.display.set_mode(SCREEN_SIZE)
finished = False

#Apple
apple_pos = 0,0

#Snake
facing = 'right'
snake = deque()
piece_size = SCREEN_SIZE[0] / GridSize
body_size = piece_size,piece_size
size = 1
MOVESNAKE = pygame.event.custom_type()

#Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


# --------------------
# To Do List
# --------------------
# Delay on create apple
# Clicking on play again after losing causes snake to become speed

def start():
    pygame.init()
    createSnake()
    makeApple()
    playGame()

def playGame():
    global facing

    playing = True

    pygame.time.set_timer(MOVESNAKE, 750)

    while playing:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                playing = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    facing = 'right' if facing == 'right' and size > 1 else 'left'
                if event.key == pygame.K_RIGHT:
                    facing = 'left' if facing == 'left' and size > 1 else 'right'
                if event.key == pygame.K_DOWN:
                    facing = 'up' if facing == 'up' and size > 1 else 'down'
                if event.key == pygame.K_UP:
                    facing = 'down' if facing == 'down' and size > 1 else 'up'

                if event.key == pygame.K_p:
                    restartGame()

            if event.type == MOVESNAKE:
                if finished:
                    moveSnake()





def createSnake():
    global Grid

    middle = floor(GridSize / 2)  # Middle of Screen
    Grid[middle][middle] = 1
    snake.append((middle,middle))
    pygame.draw.rect(screen,WHITE,((middle * piece_size, middle * piece_size),body_size))

    pygame.display.update()

def moveSnake():
    global size

    head_pos = snake[-1]

    if facing == 'up':
        head_pos = head_pos[0],head_pos[1] - 1
    if facing == 'right':
        head_pos = head_pos[0] + 1, head_pos[1]
    if facing == 'down':
        head_pos = head_pos[0], head_pos[1] + 1
    if facing == 'left':
        head_pos = head_pos[0] - 1, head_pos[1]

    #Snake eats apple can gets bigger
    if snake[0] == apple_pos:
        Grid[apple_pos[1]][apple_pos[0]] = 1
        size += 1
        makeApple()

    #Out of bounds check
    if head_pos[0] >= GridSize or head_pos[0] < 0\
            or head_pos[1] >= GridSize or head_pos[1] < 0:
        print('1', head_pos)
        endScreen()
    #Ate itself
    elif Grid[head_pos[1]][head_pos[0]] == 1:
        print('2', head_pos)
        endScreen()
    else:
        snake.append((head_pos))
        Grid[head_pos[1]][head_pos[0]] = 1
        pygame.draw.rect(screen,WHITE,((head_pos[0] * piece_size, head_pos[1] * piece_size),body_size))

    #Check whether to delete tail or not
    if size < len(snake):
        tail_pos = snake.popleft()
        Grid[tail_pos[1]][tail_pos[0]] = 0
        pygame.draw.rect(screen, BLACK, ((tail_pos[0] * piece_size, tail_pos[1] * piece_size), body_size))


    for x in Grid:
        print(x)

    print('----------------------')

    pygame.display.update()

def makeApple():
    global apple_pos, Grid

    random.seed(datetime.now())

    x,y = 0,0
    while True:
        x = random.randint(0,GridSize - 1)
        y = random.randint(0,GridSize - 1)
        print(x,y)
        if Grid[y][x] == 0:
            break

    Grid[y][x] = 2
    apple_pos = x,y

    pygame.draw.circle(screen,WHITE,((x + .5) * piece_size, (y + .5) * piece_size),piece_size / 2)

    pygame.display.update()

def endScreen():
    global finished

    pygame.draw.rect(screen,BLACK,((0,0),(SCREEN_SIZE)))

    font = pygame.font.Font('freesansbold.ttf',32)
    msg = 'You Lose     Score: ' + str(size) if size < GridSize * GridSize else 'You Win'
    playagain = 'Click p to play again'

    text = font.render(msg, True, WHITE)
    textRect = text.get_rect()
    textRect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] / 2)

    text1 = font.render(playagain,True,WHITE)
    text1Rect = text1.get_rect()
    text1Rect.center = (SCREEN_SIZE[0] / 2, SCREEN_SIZE[1] - SCREEN_SIZE[1]/GridSize)

    screen.blit(text,textRect)
    screen.blit(text1,text1Rect)

    pygame.time.set_timer(MOVESNAKE,0)
    finished = True

def restartGame():
    global  facing, size, Grid

    facing = 'right'
    size = 1
    Grid = [[0 for i in range(GridSize)] for j in range(GridSize)]
    snake.clear()

    pygame.draw.rect(screen, BLACK, ((0, 0), (SCREEN_SIZE)))

    createSnake()
    makeApple()
    pygame.time.set_timer(MOVESNAKE, 750)

    pygame.display.update()

start()