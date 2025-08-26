from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import json
import os
import pygame
from pygame import mixer

pygame.init()
mixer.init()

app = Ursina()

# Define the save file path
SAVE_FILE = "game_save.json"

player = FirstPersonController()
Sky()

boxes = []

pygame.mixer.music.load('sound/level_grzyby.mp3')
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1, 0.0, 5000)
sound_build_destroy = pygame.mixer.Sound("sound/bmove.wav")
jump = pygame.mixer.Sound("sound/jump.wav")

# Load saved blocks if the file exists
def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            saved_blocks = json.load(f)
            for block in saved_blocks:
                box = Button(
                    color=color.white,
                    model='cube',
                    position=tuple(block['position']),
                    texture=block['texture'],
                    parent=scene,
                    origin_y=0.5
                )
                boxes.append(box)

# Save the current blocks to a file
def save_game():
    saved_blocks = []
    for box in boxes:
        saved_blocks.append({
            'position': [box.x, box.y, box.z],
            'texture': box.texture.name if hasattr(box.texture, 'name') else 'grass.png'
        })
    with open(SAVE_FILE, 'w') as f:
        json.dump(saved_blocks, f)

# Load the game at startup
load_game()

# Generate the initial ground
for i in range(20):
    for j in range(20):
        box = Button(
            color=color.white,
            model='cube',
            position=(j, 0, i),
            texture='grass.png',
            parent=scene,
            origin_y=0.5
        )
        boxes.append(box)

def input(key):
    for box in boxes:
        if box.hovered:
            if key == 'left mouse down':
                new = Button(
                    color=color.white,
                    model='cube',
                    position=box.position + mouse.normal,
                    texture='grass.png',
                    parent=scene,
                    origin_y=0.5
                )
                boxes.append(new)
                sound_build_destroy.play()
                save_game()
            if key == 'right mouse down':
                boxes.remove(box)
                destroy(box)
                sound_build_destroy.play()
                save_game()
        if key == 'space':
            jump.play()

def on_application_exit():
    save_game()
    return True

app.run()