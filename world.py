import random
from OpenGL.GL import *
from sklearn.neighbors import NearestNeighbors
from Queue import Queue
class World:
  def __init__(self, width, height, amount_food):
    self.foods = []
    self.walls = []
    self.worms = []
    self.food_map = []
    self.wall_map = []
    self.width = width
    self.height = height
    self.alive_count = 0
    self.move_queue = Queue()
    self.ready_queue = Queue()
    
    self.generate_walls()
    self.generate_food(amount_food)
    
  def drawFoods(self):
    glColor3f(0.0, 1.0, 0.0)   
    size = 0.5
    glBegin(GL_QUADS)
    for food in self.foods:
      glVertex2f(food[0] + size, food[1] + size)
      glVertex2f(food[0] + size, food[1] - size)
      glVertex2f(food[0] - size, food[1] - size)
      glVertex2f(food[0] - size , food[1] + size)
    glEnd()
    
  def drawWalls(self):
    glColor3f(1.0, 0.0, 0.0)   
    glBegin(GL_POINTS)
    for wall in self.walls:
      glVertex2f(wall[0], wall[1])
    glEnd()
  
  def drawWorms(self):
    glColor3f(0.5, 0.5, 1.0)   
    size = 1
    glBegin(GL_TRIANGLES)
    for worm in self.worms:
      glVertex2f(worm.position[0], worm.position[1])
      glVertex2f(worm.position[0]+size, worm.position[1]+size)
      glVertex2f(worm.position[0]-size, worm.position[1]+size)
    glEnd()

  def draw(self):
    self.drawFoods()
    self.drawWalls()
    self.drawWorms()
    
  def find_nearest_food(self, query_position):
    if len(self.foods) == 0: return None
    result = self.nearest_food.kneighbors([query_position], 1, return_distance=True)
    distance = result[0][0][0]
    food_id = result[1][0]
    return [distance, self.foods[food_id]]
  
  def find_nearest_wall(self, query_position):
    if len(self.walls) == 0: return None
    result = self.nearest_wall.kneighbors([query_position], 1, return_distance=True)
    distance = result[0][0][0]
    wall_id = result[1][0]
    return [distance, self.walls[wall_id]]
    
  def add_worm(self, worm):
    self.worms.append(worm)
    self.alive_count += 1
    
  def remove_worm(self, worm):
    self.alive_count -= 1
    
  def remove_food(self, food_position):
    self.foods.remove(food_position)
    self.food_map[food_position[0]].remove(food_position[1])
    if len(self.foods) > 0: self.nearest_food.fit(self.foods)
    
  def update_food_map(self):
    new_food_map = []
    for x in range(0,self.width):
      new_food_map.append([])
    for food in self.foods:
      new_food_map[food[0]].append(food[1])
    self.nearest_food = NearestNeighbors(1, 100)
    self.nearest_food.fit(self.foods)
    self.food_map = new_food_map

  def update_wall_map(self):
    self.wall_map = []
    for x in range(0,self.width):
      self.wall_map.append([])
    for wall in self.walls:
      self.wall_map[wall[0]].append(wall[1])
    self.nearest_wall = NearestNeighbors(1, 100)
    self.nearest_wall.fit(self.walls)
    
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
  
  def sense(self):
    for worm in self.worms[:]:
      if worm.alive: worm.sense()
      
  def queue_move(self, worm_id, direction):
      self.move_queue.put((worm_id, direction))
      if self.move_queue.qsize() >= self.alive_count:
        self.ready_queue.put("YEAH")
  
  def do_moves(self):
    if self.alive_count <= 0: return
    for i in range(0, self.alive_count):
      try:
        move = self.move_queue.get(1)
      except Empty:
        print("The move queue was missing some elements...")
        return
      worm = self.worms[move[0]]
      worm.move(move[1])
      
  def step(self):
    self.moves = []
    self.sense()
    status = self.ready_queue.get()
    if status == "stop": return
    self.do_moves()
    
  def stop(self):
    print("Brutally killing all worms...")
    for worm in self.worms[:]:
      worm.kill()
    self.ready_queue.put("stop")
  
  