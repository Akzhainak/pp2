import pygame
import sys
import math

pygame.init()

width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Paint App")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
gray = (200, 200, 200)

canvas = pygame.Surface((width, height))
canvas.fill(white)

class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.action()

drawing = False
current_color = black
current_tool = "brush"
start_pos = None
shapes = []

def set_color_black(): global current_color; current_color = black
def set_color_red(): global current_color; current_color = red
def set_color_green(): global current_color; current_color = green
def set_color_blue(): global current_color; current_color = blue

def clear_screen():
    global shapes
    canvas.fill(white)
    shapes = []

def set_tool_brush(): global current_tool; current_tool = "brush"
def set_tool_rectangle(): global current_tool; current_tool = "rectangle"
def set_tool_square(): global current_tool; current_tool = "square"
def set_tool_right_triangle(): global current_tool; current_tool = "right_triangle"
def set_tool_equilateral_triangle(): global current_tool; current_tool = "equilateral_triangle"
def set_tool_rhombus(): global current_tool; current_tool = "rhombus"

buttons = [
    Button(10, 10, 70, 30, "Black", black, set_color_black),
    Button(90, 10, 70, 30, "Red", red, set_color_red),
    Button(170, 10, 70, 30, "Green", green, set_color_green),
    Button(250, 10, 70, 30, "Blue", blue, set_color_blue),
    
    Button(330, 10, 70, 30, "Brush", gray, set_tool_brush),
    Button(410, 10, 70, 30, "Rect", gray, set_tool_rectangle),
    Button(490, 10, 70, 30, "Square", gray, set_tool_square),
    Button(570, 10, 70, 30, "R-Tri", gray, set_tool_right_triangle),
    Button(650, 10, 70, 30, "E-Tri", gray, set_tool_equilateral_triangle),
    Button(730, 10, 70, 30, "Rhombus", gray, set_tool_rhombus),
    
    Button(width-160, 10, 70, 30, "Clear", (100, 100, 100), clear_screen),
    Button(width-80, 10, 70, 30, "Exit", (150, 50, 50), lambda: (pygame.quit(), sys.exit()))
]

def draw_right_triangle(surface, color, start, end):
    points = [start, (start[0], end[1]), end]
    pygame.draw.polygon(surface, color, points, 2)

def draw_equilateral_triangle(surface, color, start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.sqrt(dx*dx + dy*dy)
    
    angle = math.atan2(dy, dx)
    x3 = start[0] + length * math.cos(angle + math.pi/3)
    y3 = start[1] + length * math.sin(angle + math.pi/3)
    
    points = [start, end, (x3, y3)]
    pygame.draw.polygon(surface, color, points, 2)

def draw_rhombus(surface, color, start, end):
    mid_x = (start[0] + end[0]) / 2
    mid_y = (start[1] + end[1]) / 2
    
    points = [
        (mid_x, start[1]),
        (end[0], mid_y),
        (mid_x, end[1]),
        (start[0], mid_y)
    ]
    pygame.draw.polygon(surface, color, points, 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        for button in buttons:
            button.check_click(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[1] > 50:
                drawing = True
                start_pos = event.pos
                
                if current_tool == "brush":
                    pygame.draw.circle(canvas, current_color, event.pos, 3)
                    shapes.append(("brush", current_color, [event.pos], 3))

        elif event.type == pygame.MOUSEMOTION and drawing:
            if current_tool == "brush":
                pygame.draw.circle(canvas, current_color, event.pos, 3)
                if shapes and shapes[-1][0] == "brush":
                    shapes[-1][2].append(event.pos)
                else:
                    shapes.append(("brush", current_color, [event.pos], 3))

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
            drawing = False
            end_pos = event.pos
            
            if start_pos and end_pos and current_tool != "brush":
                if current_tool == "rectangle":
                    rect = pygame.Rect(
                        min(start_pos[0], end_pos[0]),
                        min(start_pos[1], end_pos[1]),
                        abs(end_pos[0] - start_pos[0]),
                        abs(end_pos[1] - start_pos[1])
                    )
                    pygame.draw.rect(canvas, current_color, rect, 2)
                    shapes.append(("rectangle", current_color, rect, 2))
                
                elif current_tool == "square":
                    size = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    rect = pygame.Rect(
                        start_pos[0],
                        start_pos[1],
                        size * (1 if end_pos[0] > start_pos[0] else -1),
                        size * (1 if end_pos[1] > start_pos[1] else -1)
                    )
                    pygame.draw.rect(canvas, current_color, rect, 2)
                    shapes.append(("square", current_color, rect, 2))
                
                elif current_tool == "right_triangle":
                    draw_right_triangle(canvas, current_color, start_pos, end_pos)
                    shapes.append(("right_triangle", current_color, (start_pos, end_pos), 2))
                
                elif current_tool == "equilateral_triangle":
                    draw_equilateral_triangle(canvas, current_color, start_pos, end_pos)
                    shapes.append(("equilateral_triangle", current_color, (start_pos, end_pos), 2))
                
                elif current_tool == "rhombus":
                    draw_rhombus(canvas, current_color, start_pos, end_pos)
                    shapes.append(("rhombus", current_color, (start_pos, end_pos), 2))

    screen.fill(white)
    screen.blit(canvas, (0, 0))
    
    pygame.draw.rect(screen, gray, (0, 0, width, 50))
    for button in buttons:
        button.draw(screen)
    
    if drawing and start_pos and current_tool != "brush":
        mouse_pos = pygame.mouse.get_pos()
        
        if current_tool == "rectangle":
            preview_rect = pygame.Rect(
                min(start_pos[0], mouse_pos[0]),
                min(start_pos[1], mouse_pos[1]),
                abs(mouse_pos[0] - start_pos[0]),
                abs(mouse_pos[1] - start_pos[1])
            )
            pygame.draw.rect(screen, current_color, preview_rect, 1)
        
        elif current_tool == "square":
            size = max(abs(mouse_pos[0] - start_pos[0]), abs(mouse_pos[1] - start_pos[1]))
            preview_rect = pygame.Rect(
                start_pos[0],
                start_pos[1],
                size * (1 if mouse_pos[0] > start_pos[0] else -1),
                size * (1 if mouse_pos[1] > start_pos[1] else -1)
            )
            pygame.draw.rect(screen, current_color, preview_rect, 1)
        
        elif current_tool == "right_triangle":
            draw_right_triangle(screen, current_color, start_pos, mouse_pos)
        
        elif current_tool == "equilateral_triangle":
            draw_equilateral_triangle(screen, current_color, start_pos, mouse_pos)
        
        elif current_tool == "rhombus":
            draw_rhombus(screen, current_color, start_pos, mouse_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()