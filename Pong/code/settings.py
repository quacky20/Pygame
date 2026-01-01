import pygame
from os.path import join

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
SIZE = {'paddle': (40, 100), 'ball': (30, 30)}
POS = {'player': (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2), 'opponent': (50, WINDOW_HEIGHT / 2), 'ball': (WINDOW_WIDTH / 2, WINDOW_HEIGHT /2), 'player_score': (WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT / 2), 'opponent_score': (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT / 2)}
SPEED = {'player': 500, 'opponent': 250, 'ball': 450}
COLORS = {
    'paddle': '#ee322c',
    'ball': '#ee622c',
    'bg': "#07242D",
    'bg-detail': "#476975"
}