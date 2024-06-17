import pygame
import logging
import random
import time

logging.basicConfig(filename='snake.log', level=logging.INFO, format='%(asctime)s  - %(message)s')

pygame.init()

WIDTH = 800
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake game")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

snake_pos = [100,50]
snake_body = [[100,50], [90,50], [80,50]]
fruit_pos = [random.randrange(1, (WIDTH// 10) ), random.randrange(1, (HEIGHT//10))]
fruit_spawn = True

direction = "RIGHT"
change_to = direction

start_time = time.time()

score = 0
max_score = 0

def read_max_score():
    try:
        with open("record.txt","r") as file:
            max_score = int(file.read())
    except FileNotFoundError:
        max_score = 0
    return max_score
max_score = read_max_score()

def draw_snake(snake_body):
    for pos in snake_body:
        pygame.draw.rect(WIN,BLACK, pygame.Rect(pos[0],pos[1],10, 10))
def draw_fruit(fruit_pos):
    pygame.draw.rect(WIN,RED, pygame.Rect(fruit_pos[0],fruit_pos[1], 10,10))

def check_colissions(snake_body):
    if snake_pos[0] < 0 or snake_pos[0] >= WIDTH or snake_pos[1] < 0 or snake_pos[1] >= HEIGHT:
        logging.info('Snake collide with the wall')
        return True
    if snake_pos in snake_body[1:]:
        logging.info("Snake collide with herself")
        return True
    return False

def draw_timer(seconds):
    font = pygame.font.SysFont(None,36)
    text = font.render(f'Time left: {15 - seconds:.1f}',True,BLACK)
    WIN.blit(text,(10,10))

def draw_score(score, max_score):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f'Score: {score} Max Score: {max_score}',True,BLACK)
    WIN.blit(text,(WIDTH - 300, 10))

paused = False
paused_time = 0

while True:
    current_time = time.time()
    elapsed_time = current_time - start_time - paused_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                logging.info("User pressed left key")
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT:
                logging.info("User pressed right key")
                change_to = "RIGHT"
            if event.key == pygame.K_UP:
                logging.info("User pressed up key")
                change_to = "UP"
            if event.key == pygame.K_DOWN:
                logging.info("User pressed down key")
                change_to = "DOWN"
            if event.key == pygame.K_SPACE:
                if not paused:
                    paused = True
                    paused_start_time = time.time()
                    logging.info("User pressed space, game is on pause")
                else:
                    paused = False
                    paused_time += time.time() - paused_start_time
                    logging.info("User pressed space, game is resumed")
    if elapsed_time >= 15:
        logging.info("Time is over, game is closed")
        pygame.quit()
    if not paused:
        if change_to == "LEFT" and direction != "RIGHT":
            direction = "LEFT"
        if change_to == "RiGHT" and direction != "LEFT":
            direction = "RiGHT"
        if change_to == "UP" and direction != "DOWN":
            direction = "UP"
        if change_to == "DOWN" and direction != "UP":
            direction = "DOWN"

        if direction == "LEFT":
            snake_pos[0] -=10
        if direction == "RIGHT":
            snake_pos[0] +=10
        if direction == "UP":
            snake_pos[1] +=10
        if direction == "DOWN":
            snake_pos[1] -=10
        if check_colissions(snake_body):
            logging.info("Game is over, snake collide with somthing")
            pygame.quit()
        snake_body.insert(0, list(snake_pos))

        if snake_pos[0] == fruit_pos[0] and snake_pos[1] == fruit_pos[1]:
            logging.info("Snake ate food")
            fruit_spawn = False
            score +=1
            if score > max_score:
                max_score = score
            start_time = time.time()
        else:
            snake_body.pop()
        if not fruit_spawn:
            fruit_pos = [random.randrange(1, (WIDTH // 10)), random.randrange(1,(HEIGHT // 10))]
            fruit_spawn = True
        WIN.fill(WHITE)
        draw_snake(snake_body)
        draw_fruit(fruit_pos)
        draw_timer(elapsed_time)
        draw_score(score, max_score)

        if paused:
            paused_time += time.time() - paused_start_time
            font = pygame.font.SysFont(None,36)
            text = font.render("Game is on pause",True, BLACK)
            WIN.blit(text,(WIDTH // 2 - 70, HEIGHT //2 - 70))
        pygame.display.flip()
        pygame.time.Clock().tick(15)

        with open ('record.txt',"w") as file:
            file.write(str(max_score))

