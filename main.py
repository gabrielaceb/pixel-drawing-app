import pygame
import sys

# Initialise PyGame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Colouring App")
canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

# Colours and brushes
PALETTE = [(0, 0, 0), (255, 0, 0), (0, 128, 0), (0, 0, 255), (255, 255, 0),
           (255, 165, 0), (255, 192, 203), (160, 32, 240)]
current_colour = PALETTE[0]

BRUSH_SHAPES = ["square", "circle", "diamond"]
brush_shape_index = 0
brush_size = 10

# Button settings
BUTTON_HEIGHT = 40
PALETTE_BUTTON_WIDTH = 40
MARGIN = 10

# Font
font = pygame.font.SysFont(None, 24)

def draw_diamond(surface, color, pos, size):
    x, y = pos
    points = [(x, y - size), (x + size, y), (x, y + size), (x - size, y)]
    pygame.draw.polygon(surface, color, points)

def draw_ui():
    # Palette buttons
    for i, color in enumerate(PALETTE):
        rect = pygame.Rect(i * (PALETTE_BUTTON_WIDTH + MARGIN) + MARGIN, HEIGHT - BUTTON_HEIGHT - MARGIN,
                           PALETTE_BUTTON_WIDTH, BUTTON_HEIGHT)
        pygame.draw.rect(screen, color, rect)
        if color == current_colour:
            pygame.draw.rect(screen, (0, 0, 0), rect, 3)

    # Brush type button
    brush_rect = pygame.Rect(WIDTH - 3 * (PALETTE_BUTTON_WIDTH + MARGIN), HEIGHT - BUTTON_HEIGHT - MARGIN,
                             PALETTE_BUTTON_WIDTH * 2, BUTTON_HEIGHT)
    pygame.draw.rect(screen, (200, 200, 200), brush_rect)
    brush_text = font.render(BRUSH_SHAPES[brush_shape_index], True, (0, 0, 0))
    screen.blit(brush_text, (brush_rect.x + 5, brush_rect.y + 10))

    # Clear button
    clear_rect = pygame.Rect(WIDTH - (PALETTE_BUTTON_WIDTH + MARGIN), HEIGHT - BUTTON_HEIGHT - MARGIN,
                             PALETTE_BUTTON_WIDTH, BUTTON_HEIGHT)
    pygame.draw.rect(screen, (220, 0, 0), clear_rect)
    clear_text = font.render("Clear", True, (255, 255, 255))
    screen.blit(clear_text, (clear_rect.x + 5, clear_rect.y + 10))

    return brush_rect, clear_rect

def handle_brush(pos):
    if BRUSH_SHAPES[brush_shape_index] == "square":
        pygame.draw.rect(canvas, current_colour, (pos[0] - brush_size, pos[1] - brush_size,
                                                  brush_size * 2, brush_size * 2))
    elif BRUSH_SHAPES[brush_shape_index] == "circle":
        pygame.draw.circle(canvas, current_colour, pos, brush_size)
    elif BRUSH_SHAPES[brush_shape_index] == "diamond":
        draw_diamond(canvas, current_colour, pos, brush_size)

# Main loop
painting = False
clock = pygame.time.Clock()

while True:
    screen.blit(canvas, (0, 0))
    brush_button, clear_button = draw_ui()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if y >= HEIGHT - BUTTON_HEIGHT - MARGIN:
                # Check palette buttons
                for i, color in enumerate(PALETTE):
                    rect = pygame.Rect(i * (PALETTE_BUTTON_WIDTH + MARGIN) + MARGIN,
                                       HEIGHT - BUTTON_HEIGHT - MARGIN,
                                       PALETTE_BUTTON_WIDTH, BUTTON_HEIGHT)
                    if rect.collidepoint(event.pos):
                        current_colour = color

                # Check brush type
                if brush_button.collidepoint(event.pos):
                    brush_shape_index = (brush_shape_index + 1) % len(BRUSH_SHAPES)

                # Clear
                if clear_button.collidepoint(event.pos):
                    canvas.fill((255, 255, 255))
            else:
                painting = True
                handle_brush(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            painting = False

        elif event.type == pygame.MOUSEMOTION:
            if painting:
                handle_brush(event.pos)

    pygame.display.flip()
    clock.tick(60)
