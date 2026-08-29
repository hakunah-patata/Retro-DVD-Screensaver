import os
os.environ['SDL_VIDEODRIVER'] = 'x11'

import pygame
import sys

# Helper function to slant text
def shear_text_surface(surf, shear=0.3):
    w, h = surf.get_size()
    new_w = w + int(abs(shear) * h)
    new_surf = pygame.Surface((new_w, h), pygame.SRCALPHA)
    for y in range(h):
        offset = int(shear * y)
        new_surf.blit(surf, (offset, y), (0, y, w, 1))
    return new_surf

# Setup

pygame.init()
INFO = pygame.display.Info()
SCREEN_W = INFO.current_w
SCREEN_H = INFO.current_h

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), pygame.FULLSCREEN)
pygame.display.set_caption("DVD Screensaver")

clock = pygame.time.Clock()
FPS = 60

# Colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

COLORS = [
    (220, 60, 60), # Red
    (220, 140, 50), # Orange
    (200, 210, 55), # Yellow-Green
    (60, 210, 90), # Green
    (55, 175, 220), # Cyan-Blue
    (90, 90, 210), # Purple
    (220, 60, 160), # Pink/Magenta
]

color_index = 0

# Fonts

font_dvd = pygame.font.Font("contm.ttf", 160)

# Logo Surface

def make_logo(color):
    dvd_surf = font_dvd.render("DVD", True, color)

    # Slant each VIDEO letter
    vid_font = pygame.font.Font("contm.ttf", 50)
    letter_surfs = []
    for char in "VIDEO":
        surf = vid_font.render(char, True, color)
        surf = shear_text_surface(surf, 0.15) # Only slants VIDEO
        letter_surfs.append(surf)

    vid_width = sum(surf.get_width() for surf in letter_surfs)
    vid_height = max(surf.get_height() for surf in letter_surfs)

    logo_w = max(dvd_surf.get_width(), vid_width) + 10
    logo_h = dvd_surf.get_height() + vid_height + 4

    surface = pygame.Surface((logo_w, logo_h), pygame.SRCALPHA)

    dvd_x = (logo_w - dvd_surf.get_width()) // 2
    surface.blit(dvd_surf, (dvd_x, 0))

    vid_x = (logo_w - vid_width) // 2
    for surf in letter_surfs:
        surface.blit(surf, (vid_x, dvd_surf.get_height() + 4))
        vid_x += surf.get_width() + 3

    return surface

logo = make_logo(COLORS[color_index])
LOGO_W = logo.get_width()
LOGO_H = logo.get_height()

# Position & Velocity

x = float(SCREEN_W // 3)
y = float(SCREEN_H // 3)

SPEED = 1.8
dx = SPEED
dy = SPEED * 0.75

# Color Helper

def next_color():
    global color_index, logo, LOGO_W, LOGO_H
    color_index = (color_index +1) % len(COLORS)
    logo = make_logo(COLORS[color_index])
    LOGO_W = logo.get_width()
    LOGO_H = logo.get_height()

# Main Loop

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
            pygame.quit()
            sys.exit()

    x += dx
    y += dy

    bounced_x = False
    bounced_y = False

    if x <= 0:
        x = 0
        dx = abs(dx)
        bounced_x = True
    elif x >= SCREEN_W -LOGO_W:
        x = SCREEN_W - LOGO_W
        dx = -abs(dx)
        bounced_x = True

    if y <= 0:
        y = 0
        dy = abs(dy)
        bounced_y = True
    elif y >= SCREEN_H - LOGO_H:
        y = SCREEN_H - LOGO_H
        dy = -abs(dy)
        bounced_y = True

    if bounced_x or bounced_y:
        next_color()

    screen.fill(BLACK)
    screen.blit(logo, (int(x), int(y)))

    pygame.display.flip()
    clock.tick(FPS)
