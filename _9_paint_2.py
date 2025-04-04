import pygame as pg
from math import cos, sin , pi 
pg.init()

eraser = (255, 255, 255)
black = (0, 0, 0)
green = (34, 139, 34)
blue = (0, 0, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)

screen = pg.display.set_mode((640, 480))
font = pg.font.SysFont("Verdana", 15)
cur_color = eraser


def get_distance(a,b): 
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

def right_triangle(screen, cur, end, d, color): 
    x1, y1, x2, y2 = cur[0], cur[1], end[0], end[1] 
    difx = abs(x1-x2) 
    dify = abs(y1-y2) 
    # if x1 <= x2: 
    if y1 < y2: 
        pg.draw.polygon(screen, color, [(x1, y1), (x1, y1 + dify), (x2, y2)], d)    
    else: 
        pg.draw.polygon(screen, color, [(x1, y1), (x1, y1 - dify), (x2, y2)], d)    
      
def triangle(color, pos):
    pg.draw.polygon(screen, color, pos, 3)

def square(screen, start, end, d, color):
    x1 = start[0]
    y1 = start[1]
    x2 = end[0]
    y2 = end[1]

    a = abs(x1-x2)
    if x1 <= x2:
        if y1 < y2:
            pg.draw.rect(screen, color, (x1, y1, a, a), d)
        else:
            pg.draw.rect(screen, color, (x1, y2, a, a), d)
    else:
        if y1 < y2:
            pg.draw.rect(screen, color, (x2, y1, a, a), d)
        else:
            pg.draw.rect(screen, color, (x2, y2, a, a), d)

def rhombus(color, pos):
    pg.draw.polygon(screen, color, pos, 3)

last_pos = (0, 0)
w = 2
draw_line = False
erase = False
ed = 50

def taskBar():
    menu = pg.image.load("menu.png")
    screen.blit(menu, (0, 0))
    
    black_rect = (10, 5, 20, 20)
    pg.draw.rect(screen, black, black_rect)
    green_rect = (30, 5, 20, 20)
    pg.draw.rect(screen, green, green_rect)
    blue_rect = (50, 5, 20, 20)
    pg.draw.rect(screen, blue, blue_rect)
    yellow_rect = (70, 5, 20, 20)
    pg.draw.rect(screen, yellow, yellow_rect)
    red_rect = (90, 5, 20, 20)
    pg.draw.rect(screen, red, red_rect)

    lineImage = pg.image.load("drawline.png")
    lineImage = pg.transform.scale(lineImage, (20, 20))
    screen.blit(lineImage, (150, 5))

    rectImage = pg.image.load("rect.png")
    rectImage = pg.transform.scale(rectImage, (30, 30))
    screen.blit(rectImage, (170, 0))

    squareImage = pg.image.load("square.png")
    squareImage = pg.transform.scale(squareImage, (30, 30))
    screen.blit(squareImage, (200, 0))

    circleImage = pg.image.load("circle.png")
    circleImage = pg.transform.scale(circleImage, (25, 25))
    screen.blit(circleImage, (230, 3))

    etrienImage = pg.image.load("etrien.png")
    etrienImage = pg.transform.scale(etrienImage, (30, 30))
    screen.blit(etrienImage, (255, 0))

    trienImage = pg.image.load("trien.png")
    trienImage = pg.transform.scale(trienImage, (30, 30))
    screen.blit(trienImage, (285, 0))

    rhombusImage = pg.image.load("rhombus.png")
    rhombusImage = pg.transform.scale(rhombusImage, (30, 30))
    screen.blit(rhombusImage, (315, 0))

    eraserImage = pg.image.load("eraser.png")
    eraserImage = pg.transform.scale(eraserImage, (30, 30))
    screen.blit(eraserImage, (600, 0))

di = {
    'sqr': False,
    'triangle': False,
    'rhombus': False,
    'right_triangle': False
}
screen.fill((0,0,0))
draw = "line"
# screen.blit(surf, (0,0))
running = True
while running:
    mouseX, mouseY = pg.mouse.get_pos()
    pos = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if(draw == "rect" and event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and mouseY > 30):
            drawRectangle(screen, pg.mouse.get_pos(), 200, 100, mode)
        if(draw == "square" and event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and mouseY > 30):
            drawSquare(screen, pg.mouse.get_pos(), 100, 100, mode)
        if(draw == "circle" and event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and mouseY > 30):
            drawCircle(screen, pg.mouse.get_pos(), mode)
        if(draw == "etrien" and event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and mouseY > 30):
            drawRightTriangle(screen, mode, pg.mouse.get_pos())
        if(draw == "trien" and event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and mouseY > 30):
            drawEquilateralTriangle(screen, mode, pg.mouse.get_pos())
        if(draw == "rhombus" and event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and mouseY > 30):
            drawRhombus(screen, mode, pg.mouse.get_pos())
        
        if(0 <= mouseY <= 30):
                if(10 <= mouseX <= 30):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        mode = black
                elif(30 <= mouseX <= 50):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        mode = green
                elif(50 <= mouseX <= 70):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        mode = blue
                elif(70 <= mouseX <= 90):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        mode = yellow
                elif(90 <= mouseX <= 110):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        mode = red
                elif(600 <= mouseX <= 630):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        mode = eraser
                elif(150 <= mouseX <= 170):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        draw = "line"
                elif(170 <= mouseX <= 200):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        draw = "rect"
                elif(200 <= mouseX <= 230):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        draw = "square"
                elif(230 <= mouseX <= 255):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        draw = "circle"
                elif(255 <= mouseX <= 285):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        draw = "etrien"
                elif(285 <= mouseX <= 315):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        draw = "trien"
                elif(315 <= mouseX <= 345):
                    if(event.type == pg.MOUSEBUTTONDOWN and event.button == 1):
                        draw = "rhombus"


        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1:
                di['sqr'] = True
                for i, j in di.items(): # for i in di.keys():
                    if i != 'sqr':
                        di[i] = False
            if event.key == pg.K_2:
                di['triangle'] = True
                for i, j in di.items():
                    if i != 'triangle':
                        di[i] = False
            if event.key == pg.K_3:
                di['rhombus'] = True
                for i, j in di.items():
                    if i != 'rhombus':
                        di[i] = False
            if event.key == pg.K_4:
                di['right_triangle'] = True
                for i, j in di.items():
                    if i != 'right_triangle':
                        di[i] = False
            
                
        elif di['sqr'] == True:
            if event.type == pg.MOUSEBUTTONDOWN:
                last_pos = pos
            if event.type == pg.MOUSEBUTTONUP:
                square(screen, last_pos, pos, w, cur_color)
        elif di['triangle'] == True:
            if event.type == pg.MOUSEBUTTONDOWN:
                last_pos = pos
            if event.type == pg.MOUSEBUTTONUP:
                d = get_distance(last_pos, pos)
                triangle(cur_color,[last_pos, pos,((pos[0] - last_pos[0])*cos(pi/3) - (pos[1] - last_pos[1])*sin(pi/3) + last_pos[0], (pos[0] - last_pos[0])*sin(pi/3) + (pos[1] - last_pos[1])*cos(pi/3) + last_pos[1])])
        if di['right_triangle'] == 1:
            if event.type == pg.MOUSEBUTTONDOWN:
                last_pos = pos
            if event.type == pg.MOUSEBUTTONUP:
                right_triangle(screen, last_pos, pos, w, cur_color)
        elif di['rhombus'] == 1:
            if event.type == pg.MOUSEBUTTONDOWN:
                last_pos = pos
            if event.type == pg.MOUSEBUTTONUP:
                d = get_distance(last_pos, pos)
                rhombus(cur_color, [last_pos, (last_pos[0] + d, last_pos[1]), (pos[0] + d, pos[1]), pos])
        txt = font.render("square - 1 right triangle - 2 rhombus - 3 equivalent triangle - 4", True, (255,0,0))
        screen.blit(txt, (0,0))

    taskBar()
    pg.display.update()
pg.quit()