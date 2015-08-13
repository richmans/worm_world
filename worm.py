class Worm:
  health = 100
  age = 0
  dna = ""
  controller = None
  position = [0,0]
  
  def __init__(self, id, dna, world, health, position):
    self.id = id
    self.world = world
    self.dna = dna
    self.health = health
    self.position = position
    
  def send(self, command, data = None):
    if self.controller != None:
      self.controller.handle_event(self.id, command, data)
      
  def kill(self):
    print("Worm %d died at age %d, health %d" % (self.id, self.age, self.health))
    self.send("kill")
    self.world.remove_worm(self)
  
  def update_position(self, direction):
    if direction == 's':
      self.position[1] += 1
    elif direction == 'n':
      self.position[1] -= 1
    elif direction == 'e':
      self.position[0] -= 1
    elif direction == 'w':
      self.position[0] += 1
  
  def check_wall(self):
    if self.world.is_wall(self.position):
      self.kill()
  
  def check_food(self):
    if self.world.is_food(self.position):
      self.health += 100
      self.world.remove_food(self.position)
      
  def check_health(self):
    if self.health <= 0:
      self.kill()
      
  def move(self, direction):
    self.update_position(direction)
    self.health -= 1
    self.age += 1
    self.check_wall()
    self.check_health()
    self.check_food()
  
  def translate_coordinates(self, target, debug = False):
    distance_multiplier = 0.3
    if debug: print("Translating from %s to %s, %d" % (self.position, coordinates, distance))
    result = [0,0,0,0]
    if target == None or target[0] == 0: 
      return result
    distance, coordinates = target
    delta_x = coordinates[0] - self.position[0]
    delta_y = coordinates[1] - self.position[1]
    if delta_y == 0:
      ratio = 1
    elif delta_x == 0:
      ratio = 0.000000000001
    else:
      ratio = float(abs(delta_x)) / (abs(delta_x) +  abs(delta_y))
      
    distance = max(1, distance * distance_multiplier)

    if delta_x > 0:
      # the object is west
      result[3] = round((255.0 / distance) * ratio)
    else:
      # the object is east
      result[1] = round((255.0 / distance) * ratio)
    
    if delta_y > 0:
      # the object is south
      result[2] = round((255.0 / distance) * (1.0-ratio))
    else:
      result[0] = round((255.0 / distance) * (1.0-ratio))
    if debug: print("Result %s" % result)
    return result
    
  def sense(self):
    nearest_food  = self.world.find_nearest_food(self.position)
    nearest_wall  = self.world.find_nearest_wall(self.position)
    food_sensors = self.translate_coordinates(nearest_food)
    wall_sensors = self.translate_coordinates(nearest_wall)
    sensors = food_sensors + wall_sensors
    self.send("sense", sensors)