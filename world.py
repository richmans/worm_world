import random
from OpenGL.GL import *

class World:
  def __init__(self, width, height, amount_food):
    self.foods = []
    self.walls = []
    self.worms = []
    self.food_map = []
    self.wall_map = []
    self.width = width
    self.height = height
    self.generate_walls()
    self.generate_food(amount_food)
  
  def drawFoods(self):
    glColor3f(0.0, 1.0, 0.0)   
    glBegin(GL_POINTS)
    for food in self.foods:
      glVertex2f(food[0], food[1])
    glEnd()
    
  def drawWalls(self):
    glColor3f(1.0, 0.0, 0.0)   
    glBegin(GL_POINTS)
    for wall in self.walls:
      glVertex2f(wall[0], wall[1])
    glEnd()
  
  def drawWorms(self):
    glColor3f(0.0, 0.0, 1.0)   
    glBegin(GL_POINTS)
    for worm in self.worms:
      glVertex2f(worm.position[0], worm.position[1])
    glEnd()

  def draw(self):
    self.drawFoods()
    self.drawWalls()
    self.drawWorms()
    
  def find_nearest_food(self, query_position):
    pass
  
  def find_nearest_food(self, query_position):
    pass
    
  def add_worm(self, worm):
    self.worms.append(worm)
    
  def remove_worm(self, worm):
    self.worms.remove(worm)
  
  def remove_food(self, food_position):
    self.foods.remove(food_position)
    self.food_map[food_position[0]].remove(food_position[1])
    
  def update_food_map(self):
    self.food_map = []
    for x in range(0,self.width):
      self.food_map.append([])
    for food in self.foods:
      self.food_map[food[0]].append(food[1])

  def update_wall_map(self):
    self.wall_map = []
    for x in range(0,self.width):
      self.wall_map.append([])
    for wall in self.walls:
      self.wall_map[wall[0]].append(wall[1])
  
  def is_wall(self, position):
    return position[1] in self.wall_map[position[0]]
  
  def is_food(self, position):
    return position[1] in self.food_map[position[0]]
    
  def generate_walls(self):
    for x in range(1,self.width):
      self.walls.append([x,0])
      self.walls.append([x,self.height-1])
    for y in range(1,self.height):
      self.walls.append([0,y])
      self.walls.append([self.width -1 , y])
    self.update_wall_map()
      
  
  def generate_food(self, amount_food):
    random.seed()
    self.foods = []
    for i in range(0,amount_food):
      x = random.randrange(1, self.width - 1)
      y = random.randrange(1, self.height - 1)
      self.foods.append([x, y])
    self.update_food_map()
  
  def simulate_step(self):
    for worm in self.worms[:]:
      worm.sense()
  
  def stop(self):
    print("Brutally killing all worms...")
    for worm in self.worms[:]:
      worm.kill()
  
  