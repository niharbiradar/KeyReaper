"""
Nihar Biradar
Key Reaper Program
March 22 2021
"""


import random
import pygame
import sys
import random
from pygame.locals import *

FPS = 30
GAME_TIME = 60

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

REAPER_SIZE = 32

GAME_OVER_FONT_SIZE = 32
SCORE_FONT_SIZE = 20
TIME_FONT_SIZE = 20
POWERUP_FONT_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 128)

GAME_OVER = 'game over'
GAME_PLAY = 'play'

SOUL_NUMBER = 10
SOUL_SIZE = 20
SOUL_RATE = 30
souls_list = []

POWERUP_RATE = 210
POWERUP_SIZE = 10
powerup_list = []
souls_spawned = 0
powerup_spawned = 0

def main():
    global DISPLAYSURF, game_over_font, score_font, clear_sound, time_font, score, reaper
    global high_score, game_state, frames_elapsed, powerup_font, clear_sound, powerup_sound
    score = 0
    high_score = 0
    game_state = GAME_OVER
    mouse_x = 0
    mouse_y = 0
    frames_elapsed = 0
    velocity = 0
    key_pressed = False

    move_up = False
    move_down = False
    move_left = False
    move_right = False
    
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Mouse Reaper")
    reaper_sound = pygame.mixer.Sound('reaper.mp3')
    game_over_sound = pygame.mixer.Sound('gameover.wav')
    clear_sound = pygame.mixer.Sound('beeps.wav')
    powerup_sound = pygame.mixer.Sound('powerup.mp3')

    reaper = pygame.draw.rect(DISPLAYSURF, BLUE, (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, REAPER_SIZE, REAPER_SIZE), 0)

    game_over_font = pygame.font.Font('freesansbold.ttf', GAME_OVER_FONT_SIZE)
    score_font = pygame.font.Font('freesansbold.ttf', SCORE_FONT_SIZE)
    time_font = pygame.font.Font('freesansbold.ttf', TIME_FONT_SIZE)
    powerup_font = pygame.font.Font('freesansbold.ttf', POWERUP_FONT_SIZE)
    

    while True:
        mouse_clicked = False
        DISPLAYSURF.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
              pygame.quit()
              sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                mouse_clicked = True

            if event.type == pygame.KEYDOWN:
                key_pressed = True
                if event.key == pygame.K_a:
                    move_left = True
                    velocity = 3
                if event.key == pygame.K_d:
                    move_right = True
                    velocity = 3
                if event.key == pygame.K_w:
                    move_up = True
                    velocity = 3
                if event.key == pygame.K_s:
                    move_down = True
                    velocity = 3

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_w:
                    move_up = False
                if event.key == pygame.K_s:
                    move_down = False
                    
        if game_state == GAME_OVER:
            display_game_over()
            if score > high_score:
                high_score = score
            display_high_score()
            if key_pressed:
                reaper_sound.play()
                score = 0
                game_state = GAME_PLAY
                spawn_souls(SOUL_NUMBER)
        elif game_state == GAME_PLAY:
            display_time()
            frames_elapsed += 1
            if velocity > 0:
                if move_left:
                    reaper.x -= velocity
                if move_right:
                    reaper.x += velocity
                if move_up:
                    reaper.y -= velocity
                if move_down:
                    reaper.y += velocity
                if reaper.x < 0:
                    reaper.x = 0
                elif reaper.x + REAPER_SIZE > WINDOW_WIDTH:
                    reaper.x = WINDOW_WIDTH - REAPER_SIZE
                if reaper.y < TIME_FONT_SIZE:
                    reaper.y = TIME_FONT_SIZE
                elif reaper.y + REAPER_SIZE > WINDOW_HEIGHT:
                    reaper.y = WINDOW_HEIGHT - REAPER_SIZE
            pygame.draw.rect(DISPLAYSURF, BLUE, reaper)
            if is_soul(mouse_x, mouse_y) or is_powerup(mouse_x, mouse_y):
                score += 1
            if frames_elapsed % SOUL_RATE == 0:
                spawn_soul()
            if frames_elapsed % POWERUP_RATE == 0:
                spawn_powerup()
            display_souls()
            display_powerup()
            display_score()
            if frames_elapsed >= (GAME_TIME * SOUL_RATE):
                frames_elapsed = 0
                reaper_sound.stop()
                game_over_sound.play()
                souls_list.clear()
                powerup_list.clear()
                pygame.time.wait(3000)
                game_state = GAME_OVER
                reaper.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
                velocity = 0
                key_pressed = False
                move_up = False
                move_down = False
                move_left = False
                move_right = False
                pygame.event.clear()
                pygame.display.update()
    
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def display_game_over():
    game_over_text = game_over_font.render('GAME OVER', True, WHITE)
    game_over_rectangle = game_over_text.get_rect()
    game_over_rectangle.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - GAME_OVER_FONT_SIZE // 2)
    DISPLAYSURF.blit(game_over_text, game_over_rectangle)
    
    mouse_click_text = game_over_font.render('Press any key to start', True, WHITE)
    mouse_click_rectangle = mouse_click_text.get_rect()
    mouse_click_rectangle.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + GAME_OVER_FONT_SIZE // 2)
    DISPLAYSURF.blit(mouse_click_text, mouse_click_rectangle)

    powerup = pygame.draw.rect(DISPLAYSURF, BLUE, (200, 150, SOUL_SIZE, SOUL_SIZE))
    powerup_text = powerup_font.render('Adds 5 to score', True, WHITE)
    powerup_rectangle = powerup_text.get_rect()
    powerup_rectangle.center = (300, 161)
    DISPLAYSURF.blit(powerup_text, powerup_rectangle)

def display_high_score():
    high_score_text = score_font.render('High Score: ' + str(high_score), True, WHITE)
    high_score_rectangle = high_score_text.get_rect()
    high_score_rectangle.center = (WINDOW_WIDTH // 2, 10)
    DISPLAYSURF.blit(high_score_text, high_score_rectangle)

def display_score():
    score_text = score_font.render('Score: ' + str(score), True, WHITE)
    score_rectangle = score_text.get_rect()
    score_rectangle.topleft = (0, 0)
    DISPLAYSURF.blit(score_text, score_rectangle)

def display_time():
    time_text = time_font.render('Time Remaining: ' + str((GAME_TIME * SOUL_RATE - frames_elapsed) // FPS), True, WHITE)
    time_rectangle = time_text.get_rect()
    time_rectangle.topright = (WINDOW_WIDTH, 0)
    DISPLAYSURF.blit(time_text, time_rectangle)

def spawn_soul():
    spawned = False
    global souls_spawned
    while not spawned:
        soul_rectangle = pygame.draw.rect(DISPLAYSURF, WHITE, (random.randint(0, WINDOW_WIDTH - SOUL_SIZE),
                                                               random.randint(SCORE_FONT_SIZE, WINDOW_HEIGHT - SOUL_SIZE), SOUL_SIZE, SOUL_SIZE))
        if soul_rectangle.collidelist(souls_list) == -1 and soul_rectangle.collidelist(powerup_list) == -1 and pygame.Rect.colliderect(reaper, soul_rectangle) == False:
            souls_list.append(soul_rectangle)
            souls_spawned += 1
            spawned = True

def spawn_souls(count):
    for x in range(0, count):
        spawn_soul()

def is_soul(x, y):
    global souls_spawned, score, clear_sound
    for soul_rectangle in souls_list:
        if soul_rectangle.collidepoint(x, y) or pygame.Rect.colliderect(reaper, soul_rectangle):
            souls_list.remove(soul_rectangle)
            souls_spawned -= 1
            if souls_spawned == 0 and powerup_spawned == 0:
                score += 10
                clear_sound.play()
                spawn_souls(SOUL_NUMBER)
            return True
    return False    

def display_souls():
    for soul_rectangle in souls_list:
        pygame.draw.rect(DISPLAYSURF, WHITE, soul_rectangle, 0)

def spawn_powerup():
    global powerup_spawned
    spawned = False
    while not spawned:
        powerup_soul = pygame.draw.rect(DISPLAYSURF, BLUE, (random.randint(0, WINDOW_WIDTH - POWERUP_SIZE),
                                                               random.randint(SCORE_FONT_SIZE, WINDOW_HEIGHT - POWERUP_SIZE), POWERUP_SIZE, POWERUP_SIZE))
        if powerup_soul.collidelist(powerup_list) == -1 and powerup_soul.collidelist(souls_list) == -1 and pygame.Rect.colliderect(reaper, powerup_soul) == False:
            powerup_list.append(powerup_soul)
            powerup_spawned += 1
            spawned = True

def is_powerup(x, y):
    global powerup_spawned, score, powerup_sound
    for powerup_soul in powerup_list:
        if powerup_soul.collidepoint(x, y) or pygame.Rect.colliderect(reaper, powerup_soul):
            powerup_list.remove(powerup_soul)
            score += 4
            powerup_sound.play()
            powerup_spawned -= 1
            if souls_spawned == 0 and powerup_spawned == 0:
                score += 10
                clear_sound.play()
                spawn_souls(SOUL_NUMBER)
            return True
    return False

def display_powerup():
    for powerup_soul in powerup_list:
        pygame.draw.rect(DISPLAYSURF, BLUE, powerup_soul, 0)

    
if __name__ == '__main__':
    main()



