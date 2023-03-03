"""A Simple Minesweeper Game, with cheats"""

# ~~~ Imports
import pygame
import random
import numpy

from typing import Tuple, List

from classes import *
from constants import *


# ~~~ Functions
def get_box_width(screen_size: Tuple[int, int], box_num: int) -> float:
    return min(screen_size) / box_num


def get_rect(pos: Point, width: int, pad: int) -> Tuple[int, int, int, int]:
    return (
        pos.x * width + pad, pos.y * width + pad, width - pad, width - pad
    )


def get_mouse_index() -> Tuple[int, int]:
    mouse_x, mouse_y = pygame.mouse.get_pos()

    mouse_x = int(numpy.floor(mouse_x / width))
    mouse_y = int(numpy.floor(mouse_y / width))
    
    return mouse_x, mouse_y


def expand_0s(init_box: Box, seen: List | None = None):
    if seen is None:
        seen = []
    
    if init_box.num == 0:
        for point in init_box.get_neighbours(NUM_BOXES):
            if point not in seen:
                box = BOXES[point.x][point.y]
                
                box.revealed = True
                seen.append(point)
                
                expand_0s(box, seen)
                

def get_boxes(boxes: List[List[Box]], points: List[Point]) -> List[Box]:
    return [boxes[i.x][i.y] for i in points]


# ~~~ Setup
pygame.init()

# Clock
CLOCK = pygame.time.Clock()
# Screen
screen = pygame.display.set_mode(INIT_SIZE, pygame.RESIZABLE)
# Font
pygame.font.init()
FONT_SIZES = {
    size: pygame.font.SysFont(FONT_NAME, size) for size in range(FONT_MIN_SIZE, FONT_MAX_SIZE + 1)
}

FONT_NUMBER_BY_SIZE = {
    size: {
        n: FONT_SIZES[size].render(str(n), True, BLACK) for n in range(0, 9)
    } for size in range(FONT_MIN_SIZE, FONT_MAX_SIZE + 1)
}

# Boxes
BOXES: List[List[Box]] = [[] for _ in range(NUM_BOXES)]
for x in range(NUM_BOXES):
    for y in range(NUM_BOXES):
        BOXES[x].append(
            Box(Point(x, y), mine=random.random() <= MINE_PROBABILITY)
        )

# Numbers
for x in range(NUM_BOXES):
    for y in range(NUM_BOXES):
        BOXES[x][y].num = sum(map(
            lambda x: BOXES[x.x][x.y].is_mine,
            BOXES[x][y].get_neighbours(NUM_BOXES)
        ))

# ~~~ Main Game Loop
RUNNING = True
while RUNNING:
    width = int(get_box_width(screen.get_size(), NUM_BOXES))

    # Check events
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT | pygame.WINDOWCLOSE:
                RUNNING = False

            # Handle clicks
            case pygame.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                mouse_x, mouse_y = get_mouse_index()

                if right:
                    if 0 <= mouse_x < NUM_BOXES and 0 <= mouse_y < NUM_BOXES:
                        box = BOXES[mouse_x][mouse_y]
                        
                        if not box.revealed:
                            box.is_flag = not box.is_flag

                if left:
                    if 0 <= mouse_x < NUM_BOXES and 0 <= mouse_y < NUM_BOXES:
                        box = BOXES[mouse_x][mouse_y]
                        if box.is_mine:
                            RUNNING = False
                        
                        if not box.is_flag:
                            if box.revealed:
                                # Chording
                                neighbours = get_boxes(BOXES, box.get_neighbours(NUM_BOXES))
                                if sum(map(lambda x: x.is_flag, neighbours)) == box.num:
                                    for _box in neighbours:
                                        if not _box.is_flag:
                                            _box.revealed = True
                                            
                                        if _box.num == 0:
                                            expand_0s(_box)
                            else:
                                box.revealed = True
                                
                                if box.num == 0:
                                    expand_0s(box)

    # Set background
    screen.fill(GREY)

    # Draw boxes
    for x in range(NUM_BOXES):
        for y in range(NUM_BOXES):
            box = BOXES[x][y]
            _mine = box.is_mine
            _flag = box.is_flag

            if _flag:
                colour = GREEN
            elif box.revealed:
                colour = DARK_GREY
                
                if box.num == 0:
                    colour = GREY
            else:
                colour = BLUE

            pygame.draw.rect(
                screen, colour, get_rect(Point(x, y), width, PAD)
            )

            if box.revealed and box.num > 0:
                font_num = FONT_NUMBER_BY_SIZE[30][box.num]
                
                half_num_width = int(font_num.get_width() / 2)
                half_num_height = int(font_num.get_height() / 2)
                half_box_width = int(width / 2)
                
                screen.blit(font_num, (
                    x * width + PAD + (half_box_width - half_num_width),
                    y * width + PAD + (half_box_width - half_num_height)
                ))

    # Update
    pygame.display.flip()
    CLOCK.tick(FPS)
