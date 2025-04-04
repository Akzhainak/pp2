import pygame

pygame.init()

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Animating Background")

background_img = pygame.image.load("AnimatedStreet.png").convert()

background_y = 0

def animate_background():
    global background_y
    screen.blit(background_img, (0, background_y))
    screen.blit(background_img, (0, background_y - screen_height))
    background_y += 0.5
    if background_y == screen_height:
        background_y = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    animate_background()
    
    pygame.display.update()

pygame.quit()