import os
import pygame

if os.path.exists("happy.mp3"):
    print("happy.mp3 file exists!")
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.load("happy.mp3")
    pygame.mixer.music.play()
else:
    print("happy.mp3 file does not exist!")


