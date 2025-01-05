from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

width = 500
height = 500
box_details = [50, 200, 100, 10]
box_details2 = [200, 300, 100, 10]
box_details3 = [350, 200, 100, 10]
grass_state = 0
is_day = True
radius = 10  # radius change
radius_change = 1  # circle size change
original_radius = 10
max_radius = 20  # max radius
circleinfo = [random.randint(0, 500), 500]
count = 1
speed = 5
disappear_start_time = -1
disappear_start_time2 = -1
mushrooms = [10, random.choice([1, 500]), 30, 25, 10]
mushroom_speed = 5
playerball = [250, 120]  # x, y
gravity = 2  # Gravity strength
ground_level = 20  
pause = False
life = 3
score = 0
in_air = False
game_over = False

def circleDrawing(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, -y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()

def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def convert_to_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def convert_from_zone0(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, zone)
    plot_point(x0, y0)
    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = convert_from_zone0(x, y, zone)
        plot_point(x0, y0)

def drawBox(x, y, width, height):
    for i in range(x, x + width + 1):
        midpoint_line(i, y, i, y + height)

def update_grass(value):
    global grass_state
    grass_state += 1
    glutPostRedisplay()
    glutTimerFunc(2000, update_grass, 0)

def drawgrass(startingX, endingX):
    for i in range(startingX, endingX + 1, 5):
        if grass_state % 2 == 0:
            midpoint_line(i, 0, i, 10)
        else:
            midpoint_line(i, 0, i + 5, 10)

def dayNight(value=0):
    global is_day
    if is_day:
        glClearColor(0.529, 0.808, 0.922, 1.0)
    else:
        glClearColor(0.0, 0.0, 0.0, 1.0)
    
    is_day = not is_day
    glutPostRedisplay()
    glutTimerFunc(10000, dayNight, 0)

def specialCircle(value):
    global radius, radius_change, max_radius, original_radius, circleinfo, speed, disappear_start_time, disappear_start_time2, pause
    if pause:
        return

    if radius >= max_radius and radius_change > 0:
        radius_change = -radius_change
    elif radius <= original_radius and radius_change < 0:
        radius_change = -radius_change

    if (
        (circleinfo[0] > 50 and circleinfo[0] < 150 and circleinfo[1] == 220) or
        (circleinfo[0] > 200 and circleinfo[0] < 300 and circleinfo[1] == 320) or
        (circleinfo[0] > 350 and circleinfo[0] < 450 and circleinfo[1] == 220) or
        (circleinfo[1] == 20)
    ):
        if disappear_start_time == -1:
            disappear_start_time = glutGet(GLUT_ELAPSED_TIME)
        radius_change = 0
        radius = 10
        speed = 0

    if disappear_start_time != -1 and (glutGet(GLUT_ELAPSED_TIME) - disappear_start_time) >= 2000:
        radius = 0
        if disappear_start_time2 == -1:
            disappear_start_time2 = glutGet(GLUT_ELAPSED_TIME)

    if disappear_start_time2 != -1 and (glutGet(GLUT_ELAPSED_TIME) - disappear_start_time2) >= 10000:
        circleinfo[1] = 500
        circleinfo[0] = random.randint(0, 500)
        radius = 5
        radius_change = 1
        speed = 5
        disappear_start_time = -1
        disappear_start_time2 = -1

    radius += radius_change
    circleinfo[1] -= speed

    if circleinfo[1] < 0:
        circleinfo[1] = 500
        circleinfo[0] = random.randint(0, 500)

    glutPostRedisplay()
    glutTimerFunc(100, specialCircle, 0)

def makeMushroom():
    global mushrooms
    glColor3f(1.0, 0.0, 0.0)
    circleDrawing(mushrooms[0], mushrooms[1], mushrooms[2])
    for i in range(0, mushrooms[0]):
        circleDrawing(mushrooms[0] - i, mushrooms[1], mushrooms[2])
    glColor3f(0.4, 0.2, 0)
    glPointSize(5.0)
    midpoint_line(mushrooms[1], mushrooms[3], mushrooms[1], mushrooms[4])
    glPointSize(2.0)

def motionMushroom():
    global mushrooms, mushroom_speed

    mushrooms[1] += mushroom_speed

    if mushrooms[1] < -50 or mushrooms[1] > width + 50:
        mushrooms[1] = random.choice([1, 500])
        mushroom_speed = abs(mushroom_speed) if mushrooms[1] == 1 else -abs(mushroom_speed)

def updateMushroom(value):
    global mushrooms, mushroom_speed, pause

    if pause:
        return

    motionMushroom()
    glutPostRedisplay()
    glutTimerFunc(100, updateMushroom, 0)

def drawplayer():
    global playerball
    glColor3f(0.0, 0.0, 1.0)
    circleDrawing(10, playerball[0], playerball[1])
    for i in range(0, 10):
        circleDrawing(10 - i, playerball[0], playerball[1])
    glColor3f(1.0, 0.0, 1.0)

def start_over():
    global playerball, mushrooms, circleinfo, radius, radius_change, speed, disappear_start_time, disappear_start_time2, grass_state, is_day, pause, life, score, game_over

    playerball = [250, 120]
    life = 3
    score = 0
    game_over = False
    pause = False
    grass_state = 0

    mushrooms = [10, random.choice([1, 500]), 30, 25, 10]
    mushroom_speed = 5

    circleinfo = [random.randint(0, 500), 500]
    radius = 10
    radius_change = 1
    speed = 5

    disappear_start_time = -1
    disappear_start_time2 = -1

    is_day = False
    glClearColor(0.0, 0.0, 0.0, 1.0)

    glutPostRedisplay()

def applyGravity(value):
    global playerball, gravity, ground_level, pause, in_air, life, game_over, circleinfo, radius, disappear_start_time

    if pause or game_over:
        return

    point_scored()

    # Check if the player touches the dynamic ball to gain a life
    dynamic_ball_radius = radius
    dynamic_ball_x = circleinfo[0]
    dynamic_ball_y = circleinfo[1]

    if (
        (dynamic_ball_x - dynamic_ball_radius <= playerball[0] <= dynamic_ball_x + dynamic_ball_radius) and
        (dynamic_ball_y - dynamic_ball_radius <= playerball[1] <= dynamic_ball_y + dynamic_ball_radius)
    ):
        if life < 3:
            life += 1
            print(f"Life gained! Current lives: {life}")
            # Make the dynamic ball disappear
            circleinfo = [random.randint(0, 500), -500]  
            radius = 0
            disappear_start_time = -1  # Reset the disappear timer

    if (
        (playerball[0] > 45 and playerball[0] < 155 and playerball[1] == 220) or
        (playerball[0] > 195 and playerball[0] < 305 and playerball[1] == 320) or
        (playerball[0] > 345 and playerball[0] < 455 and playerball[1] == 220) or
        (playerball[1] == 20)
    ):
        gravity = 0
    else:
        gravity = 2

    if playerball[1] > ground_level:
        playerball[1] -= gravity
    else:
        playerball[1] = ground_level

    if playerball[1] == ground_level and in_air:
        in_air = False

    glutPostRedisplay()
    glutTimerFunc(50, applyGravity, 0)

def point_scored():
    global playerball, mushrooms, score, life, in_air, game_over

    player_x, player_y = playerball
    player_radius = 10

    mushroom_radius = mushrooms[0]
    mushroom_x = mushrooms[1]
    mushroom_top = mushrooms[2] + mushrooms[0] 
    mushroom_bottom = mushrooms[2] - mushrooms[0] 

    touching_top = (mushroom_x - mushroom_radius <= player_x <= mushroom_x + mushroom_radius) and \
                   (mushroom_top - player_radius <= player_y <= mushroom_top + player_radius)

    touching_sides = (
        (player_x + player_radius > mushroom_x - mushroom_radius and player_x < mushroom_x - mushroom_radius) or 
        (player_x - player_radius < mushroom_x + mushroom_radius and player_x > mushroom_x + mushroom_radius)
    ) and (mushroom_bottom <= player_y <= mushroom_top)

    if not in_air:
        if touching_top:
            score += 1
            print(f"Point scored! Current score: {score}")
            mushrooms = [10, random.choice([1, 500]), 30, 25, 10]  
            in_air = True
        elif touching_sides:
            life -= 1
            print(f"Life reduced! Remaining lives: {life}")
            playerball = [250, 250]
            in_air = True
            if life <= 0:
                game_over = True

    if in_air and player_y == ground_level:
        in_air = False

def draw_res():
    glColor3f(0.0, 0.5, 0.8)
    midpoint_line(30, 490, 5, 470)
    midpoint_line(5, 470, 60, 470)

def draw_cross():
    glColor3f(1.0, 0.0, 0.0)
    midpoint_line(460, 490, 490, 450)
    midpoint_line(460, 450, 490, 490)

def draw_pause():
    global pause
    glColor3f(1.0, 1.0, 0.0)
    if pause:
        midpoint_line(230, 490, 280, 470)
        midpoint_line(280, 470, 230, 450)
        midpoint_line(230, 450, 230, 490)
    else:
        midpoint_line(250, 490, 250, 450)
        midpoint_line(270, 490, 270, 450)

def keyboardlistener(key, x, y):
    global pause
    if key == b'w':
        playerball[1] += 30
    if key == b'a':
        if playerball[0] <= 0:
            playerball[0] = 0
        else:
            playerball[0] -= 10
    if key == b'd':
        if playerball[0] >= 500:
            playerball[0] = 500
        else:
            playerball[0] += 10
    if key == b' ':
        pause = not pause
        if not pause:
            glutTimerFunc(100, specialCircle, 0)
            glutTimerFunc(100, updateMushroom, 0)
            glutTimerFunc(50, applyGravity, 0)

def mouseListener(button, state, x, y):
    global height, width, pause

    nx = x
    ny = height - y

    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            if nx > 230 and nx < 280 and ny > 450 and ny < 490:
                pause = not pause
                if not pause:
                    glutTimerFunc(100, specialCircle, 0)
                    glutTimerFunc(100, updateMushroom, 0)
                    glutTimerFunc(50, applyGravity, 0)
            elif nx > 5 and nx < 60 and ny > 450 and ny < 490:
                start_over()
            elif nx > 460 and nx < 490 and ny > 450 and ny < 490:
                print("Goodbye")
                glutDestroyWindow(wind)

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def display():
    global score, life, game_over

    glClear(GL_COLOR_BUFFER_BIT)  # Clear the screen
    draw_res()
    draw_cross()
    draw_pause()
    # Draw the boxes using box_details
    glColor3f(0.47, 0.09, 0.09)
    drawBox(box_details[0], box_details[1], box_details[2], box_details[3])
    drawBox(box_details2[0], box_details2[1], box_details2[2], box_details2[3])
    drawBox(box_details3[0], box_details3[1], box_details3[2], box_details3[3])

    makeMushroom()

    drawplayer()

    circleDrawing(radius, circleinfo[0], circleinfo[1])

    glColor3f(0, 0.30, 0)
    drawgrass(0, 500)

    glColor3f(1.0, 1.0, 1.0)
    draw_text(120, 470, f"Score: {score}")
    draw_text(350, 470, f"Lives: {life}")

    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        draw_text(width // 2 - 50, height // 2, f"GAME OVER\nScore: {score}")

    glFlush()  

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, width, 0, height) 
    glutTimerFunc(100, specialCircle, 0)
    glutTimerFunc(100, updateMushroom, 0)  
    glutTimerFunc(50, applyGravity, 0)

glutInit() 
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)  
glutInitWindowSize(width, height)  
glutInitWindowPosition(100, 100) 
wind = glutCreateWindow(b"OpenGL Window")  
init()
glPointSize(2.0)  
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glutDisplayFunc(display)
glutIdleFunc(display)  
glutTimerFunc(1000, update_grass, 0)
glutTimerFunc(10000, dayNight, 0)
glutKeyboardFunc(keyboardlistener)
glutMouseFunc(mouseListener)
glutMainLoop()