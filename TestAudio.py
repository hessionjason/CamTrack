import pygame
import time

# Initialize the mixer
pygame.mixer.init()

# Load sound
alert_sound = r'C:\PersonalProjects\pythonProject\SensorSound.mp3'  # Path to your alert sound file

# Play the sound
pygame.mixer.music.load(alert_sound)
pygame.mixer.music.play()

# Wait while the sound is playing
while pygame.mixer.music.get_busy():  # Check if the sound is still playing
    time.sleep(1)  # Pause the program for 1 second
