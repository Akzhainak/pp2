import pygame
import time

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mickey clock")

background = pygame.image.load("clock.png")
min_hand = pygame.image.load("min_hand.png")
sec_hand = pygame.image.load("sec_hand.png")

center = (screen_width // 2, screen_height // 2)

def rotate_hand(image, angle, pivot):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_rect = rotated_image.get_rect(center=pivot)
    return rotated_image, rotated_rect

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    crrt_tm = time.localtime()
    minutes = crrt_tm.tm_min
    seconds = crrt_tm.tm_sec
    
    min_angle = -(minutes * 6)
    sec_angle = -(seconds * 6)
    
    screen.blit(background, (0, 0))
    
    rotated_right_hand, min_rect = rotate_hand(min_hand, min_angle, center)
    screen.blit(rotated_right_hand,min_rect)
    
    rotated_left_hand, sec_rect = rotate_hand(sec_hand, sec_angle, center)
    screen.blit(rotated_left_hand, sec_rect)
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()