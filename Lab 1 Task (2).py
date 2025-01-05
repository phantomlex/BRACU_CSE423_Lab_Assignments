from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import sys

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Raindrop properties
raindrops = []
NUM_RAINDROPS = 100

# Add at top with other globals
RAIN_ANGLE = 0.0  # Controls rain direction
MAX_ANGLE = 1.0   # Maximum angle of rain deviation

# Add at top with other globals
TIME_OF_DAY = 1.0  # 0.0 is night, 1.0 is day
TRANSITION_SPEED = 0.02

def lerp_color(c1, c2, t):
    """Linear interpolation between two colors"""
    return [a + (b - a) * t for a, b in zip(c1, c2)]

# Color definitions
DAY_SKY = [0.0, 0.0, 0.0]  # Black
NIGHT_SKY = [0.7, 0.9, 1.0]  # Light blue
DAY_HOUSE = [0.8, 0.5, 0.0]  # Brown
NIGHT_HOUSE = [0.4, 0.25, 0.0]  # Dark brown
DAY_ROOF = [1.0, 0.0, 0.0]  # Red
NIGHT_ROOF = [0.5, 0.0, 0.0]  # Dark red
DAY_RAIN = [0.5, 0.5, 1.0]  # Light blue
NIGHT_RAIN = [0.2, 0.2, 0.4]  # Dark blue

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-400, 400, -300, 300)

def draw_house():
    # Get interpolated colors based on time of day
    house_color = lerp_color(NIGHT_HOUSE, DAY_HOUSE, TIME_OF_DAY)
    roof_color = lerp_color(NIGHT_ROOF, DAY_ROOF, TIME_OF_DAY)
    
    # Main house body (wider square)
    glColor3f(*house_color)
    glBegin(GL_TRIANGLES)
    # Front wall
    glVertex2f(-150, -100)  # Increased from -100 to -150
    glVertex2f(150, -100)   # Increased from 100 to 150
    glVertex2f(150, 100)
    
    glVertex2f(-150, -100)
    glVertex2f(-150, 100)
    glVertex2f(150, 100)
    glEnd()
    
    # Wider roof
    glColor3f(*roof_color)
    glBegin(GL_TRIANGLES)
    glVertex2f(-170, 100)   # Increased from -120 to -170
    glVertex2f(170, 100)    # Increased from 120 to 170
    glVertex2f(0, 200)
    glEnd()
    
    # Door
    glColor3f(0.5, 0.3, 0.0)  # Brown
    glBegin(GL_LINES)
    glVertex2f(-30, 0)
    glVertex2f(-30, -100)
    glVertex2f(30, -100)
    glVertex2f(30, 0)
    glVertex2f(-30, 0)
    glVertex2f(30, 0)
    glEnd()

    glColor3f(0.0, 0.0, 0.0)  # Black door knob
    glBegin(GL_LINES)
    glVertex2f(-400, 0)
    glVertex2f(400, 0)
    glEnd()
    glColor3f(0.0, 0.0, 0.0)  # Black door knob
    glBegin(GL_LINES)
    glVertex2f(0, -300)
    glVertex2f(0, 300)
    glEnd()    # Add window


    glColor3f(0.7, 0.7, 1.0)  # Light blue window
    glBegin(GL_LINES)
    # Window frame
    glVertex2f(50, 0)     # Left vertical
    glVertex2f(50, 50)
    glVertex2f(100, 0)    # Right vertical
    glVertex2f(100, 50)
    glVertex2f(50, 0)     # Bottom horizontal
    glVertex2f(100, 0)
    glVertex2f(50, 50)    # Top horizontal
    glVertex2f(100, 50)
    # Window cross
    glVertex2f(75, 0)     # Vertical divider
    glVertex2f(75, 50)
    glVertex2f(50, 25)    # Horizontal divider
    glVertex2f(100, 25)
    glEnd()

def draw():
    # Set background color based on time of day
    bg_color = lerp_color(DAY_SKY, NIGHT_SKY, TIME_OF_DAY)
    glClearColor(*bg_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    draw_house()
    
    # Draw raindrops
    for drop in raindrops:
        drop.draw()
        
    glutSwapBuffers()

class Raindrop:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = random.uniform(-400, 400)
        self.y = 300
        self.speed = random.uniform(2, 5)
        
    def update(self):
        # Update position using angle
        self.x += self.speed * RAIN_ANGLE  # Horizontal movement based on angle
        self.y -= self.speed
        if self.y < -300 or self.x < -400 or self.x > 400:
            self.reset()
            
    def draw(self):
        rain_color = lerp_color(NIGHT_RAIN, DAY_RAIN, TIME_OF_DAY)
        glColor3f(*rain_color)
        glBegin(GL_LINES)
        # Draw raindrop with angle
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + (10 * RAIN_ANGLE), self.y - 10)  # Angled rain
        glEnd()

def update(value):
    for drop in raindrops:
        drop.update()
    glutPostRedisplay()
    glutTimerFunc(16, update, 0)  # 60 FPS

def keyboard(key, x, y):
    global RAIN_ANGLE
    
    if key == GLUT_KEY_LEFT:
        RAIN_ANGLE = max(RAIN_ANGLE - 0.1, -MAX_ANGLE)
    elif key == GLUT_KEY_RIGHT:
        RAIN_ANGLE = min(RAIN_ANGLE + 0.1, MAX_ANGLE)
    
    glutPostRedisplay()

def keyboard_normal(key, x, y):
    global TIME_OF_DAY
    
    key = key.decode('utf-8').lower()
    if key == 'd':  # Transition to day
        TIME_OF_DAY = min(1.0, TIME_OF_DAY + TRANSITION_SPEED)
    elif key == 'n':  # Transition to night
        TIME_OF_DAY = max(0.0, TIME_OF_DAY - TRANSITION_SPEED)
    
    glutPostRedisplay()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"House with Rain")
    
    init()
    
    # Initialize raindrops
    for _ in range(NUM_RAINDROPS):
        raindrops.append(Raindrop())
    
    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard_normal)  # Add normal keyboard handler
    glutSpecialFunc(keyboard)  # Keep special keyboard handler for arrows
    glutTimerFunc(0, update, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()


