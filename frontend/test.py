import pygame

# Initialize the mixer
pygame.mixer.init()

# Load the MP3 file
pygame.mixer.music.load("sad.mp3")

# Play the MP3 file
pygame.mixer.music.play()

# Keep the script running until the music finishes
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)
