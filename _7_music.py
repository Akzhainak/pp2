import pygame
import os

pygame.init()

screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("music player")
background = pygame.image.load("blackpink.webp")
background = pygame.transform.scale(background, (500, 500))

music_folder = "." 
tracks = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]


if not tracks:
    print("No music files found")
    pygame.quit()
    exit()

current_track = 0
playing = True
track_position = 0

pygame.mixer.music.load(os.path.join(music_folder, tracks[current_track]))
pygame.mixer.music.play()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        
        if event.type == pygame.KEYDOWN:
           
           if event.key == pygame.K_w:
                if not playing:
                    pygame.mixer.music.play(start=track_position)
                    playing = True
                    
           if event.key == pygame.K_s:
                track_position = pygame.mixer.music.get_pos()/1000
                pygame.mixer.music.stop()
                playing = False
            
           if event.key == pygame.K_d:
                current_track = (current_track +1) % len(tracks)
                pygame.mixer.music.load(os.path.join(music_folder, tracks[current_track]))
                pygame.mixer.music.play()
                playing = True
            
           if event.key == pygame.K_a:
                current_track = (current_track -1) % len(tracks)
                pygame.mixer.music.load(os.path.join(music_folder, tracks[current_track]))
                pygame.mixer.music.play()
                playing = True
    screen.blit(background, (0,0))
    pygame.display.flip()
