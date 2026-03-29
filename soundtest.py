from just_playback import Playback
import pygame
import time

pygame.mixer.init()

def wake_speaker():
    # 50 ms of silence
    beep = pygame.mixer.Sound("test-files/tone-440-100.wav")
    beep.play()
    time.sleep(0.13)

def play_sound(path):
    wake_speaker()
    sound = pygame.mixer.Sound(path)
    sound.play()
    while pygame.mixer.get_busy():
        time.sleep(0.01)

# play_sound("test-files/datapad1.wav")

wake = Playback("test-files/tone-440-100.wav")
click = Playback("test-files/datapad1.wav")
wake.play()
time.sleep(0.1)
click.play()
time.sleep(1)