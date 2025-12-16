import pygame
import sys
from PIL import Image
from collections import Counter

pygame.init()
pygame.display.set_caption("Pixel Drawing App")

WIDTH, HEIGHT = 1000, 750
PALETTE_HEIGHT = 60
UI_HEIGHT = 60
CANVAS_HEIGHT = HEIGHT - PALETTE_HEIGHT - UI_HEIGHT

screen = pygame.display.set_mode((WIDTH, HEIGHT))
canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
canvas.fill((255, 255, 255))

pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONDOWN,
                          pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION,
                          pygame.DROPFILE])

BRUSH_SIZES = [4, 8, 16, 32]
BRUSH_SHAPES = ["square", "circle", "diamond"]

palette_colours = [(0, 0, 0), (255, 255, 255)]
current_colour = palette_colours[0]

brush_size_index = 1
brush_shape_index = 0
uploaded_image_path = None

font = pygame.font.SysFont("Arial", 18)

# ---------------- Functions ---------------- #

def draw_brush(x, y):
    size = BRUSH_SIZES[brush_size_index]
    shape = BRUSH_SHAPES[brush_shape_index]

    if shape == "square":
        pygame.draw.rect(canvas, current_colour,
                         (x - size//2, y - size//2, size, size))
    elif shape == "circle":
        pygame.draw.circle(canvas, current_colour, (x, y), size//2)
    elif shape == "diamond":
        points = [
            (x, y - size//2),
            (x + size//2, y),
            (x, y + size//2),
            (x - size//2, y)
        ]
        pygame.draw.polygon(canvas, current_colour, points)

def draw_palette():
    block_width = WIDTH // len(palette_colours)
    for i, colour in enumerate(palette_colours):
        rect = pygame.Rect(i * block_width, HEIGHT - PALETTE_HEIGHT,
                           block_width, PALETTE_HEIGHT)
        pygame.draw.rect(screen, colour, rect)
        if colour == current_colour:
            pygame.draw.rect(screen, (120, 120, 120), rect, 3)

def draw_buttons():
    labels = [
        ("Brush", 10),
        ("Size", 160),
        ("Use Palette", 310),
        ("Save", 480),
        ("Clear", 610),
        ("Drop Image Here", 740)
    ]

    for label, x in labels:
        rect = pygame.Rect(x, CANVAS_HEIGHT + 10, 140, 40)
        pygame.draw.rect(screen, (230, 230, 230), rect, border_radius=8)
        pygame.draw.rect(screen, (180, 180, 180), rect, 2, border_radius=8)
        text = font.render(label, True, (0, 0, 0))
        screen.blit(text, (x + 10, CANVAS_HEIGHT + 20))

def extract_palette(path, num_colours=8):
    img = Image.open(path).convert("RGB").resize((64, 64))
    pixels = list(img.getdata())
    common = Counter(pixels).most_common(num_colours)
    return [col for col, _ in common]

def draw_brush_preview(pos):
    x, y = pos
    if y > CANVAS_HEIGHT:
        return

    size = BRUSH_SIZES[brush_size_index]
    shape = BRUSH_SHAPES[brush_shape_index]

    if shape == "square":
        pygame.draw.rect(screen, current_colour,
                         (x - size//2, y - size//2, size, size), 1)
    elif shape == "circle":
        pygame.draw.circle(screen, current_colour, (x, y), size//2, 1)
    elif shape == "diamond":
        points = [
            (x, y - size//2),
            (x + size//2, y),
            (x, y + size//2),
            (x - size//2, y)
        ]
        pygame.draw.polygon(screen, current_colour, points, 1)

# ---------------- Main Loop ---------------- #

drawing = False
clock = pygame.time.Clock()

while True:
    screen.fill((245, 245, 245))
    screen.blit(canvas, (0, 0))

    draw_buttons()
    draw_palette()
    draw_brush_preview(pygame.mouse.get_pos())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.DROPFILE:
            uploaded_image_path = event.file
            palette_colours = extract_palette(uploaded_image_path)
            current_colour = palette_colours[0]

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            if y < CANVAS_HEIGHT:
                drawing = True
                draw_brush(x, y)

            elif CANVAS_HEIGHT + 10 <= y <= CANVAS_HEIGHT + 50:
                if 10 <= x <= 150:
                    brush_shape_index = (brush_shape_index + 1) % len(BRUSH_SHAPES)
                elif 160 <= x <= 300:
                    brush_size_index = (brush_size_index + 1) % len(BRUSH_SIZES)
                elif 310 <= x <= 450 and uploaded_image_path:
                    palette_colours = extract_palette(uploaded_image_path)
                    current_colour = palette_colours[0]
                elif 480 <= x <= 600:
                    pygame.image.save(canvas, "drawing_output.png")
                elif 610 <= x <= 730:
                    canvas.fill((255, 255, 255))

            elif y >= HEIGHT - PALETTE_HEIGHT:
                block_width = WIDTH // len(palette_colours)
                index = x // block_width
                if 0 <= index < len(palette_colours):
                    current_colour = palette_colours[index]

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        elif event.type == pygame.MOUSEMOTION and drawing:
            x, y = pygame.mouse.get_pos()
            if y < CANVAS_HEIGHT:
                draw_brush(x, y)

    pygame.display.flip()
    clock.tick(60)
