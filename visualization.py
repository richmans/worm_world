from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

class Visualization:
  def __init__(self, simulation):
    self.simulation = simulation
    self.setup()

  def refresh2d(self):
    glViewport(0, 0, self.width * self.zoom, self.height * self.zoom)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, self.width * self.zoom, 0.0, self.height * self.zoom, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

  def setup(self):
    self.width = self.simulation.width
    self.height = self.simulation.height
    self.zoom = 1
    if self.width < 200:
      self.zoom = 4
    glutInit()                                             # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(self.width * self.zoom, self.height * self.zoom)                      # set window size
    glutInitWindowPosition(0, 0)                           # set window position
    self.window = glutCreateWindow("Worm World")                # create window with title
    glutDisplayFunc(self.draw)                             # set draw function callback
    glutIdleFunc(self.draw)                                # draw all the time
    glutKeyboardFunc(self.handle_keyboard)
  
  def handle_keyboard(self, key, x, y):
    if key == 'q':
      self.simulation.stop()

    
  def run(self):
    glutMainLoop()

  def check_exit(self):
    if self.simulation.finished:  sys.exit(0)
    
  def draw(self):
    if self.simulation.sim_world == None: return
    self.check_exit()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    self.refresh2d()  
    glScalef(self.zoom, self.zoom, self.zoom)
    self.simulation.sim_world.draw()                                  # draw the whole world! 
    
    glutSwapBuffers()                                  # important for double buffering
    
    