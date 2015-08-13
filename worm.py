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
    print("Worm %d died at age %d" % (self.id, self.age))
    self.send("kill")
    self.world.remove_worm(self)
  
  def update_position(self, direction):
    if direction == 's':
      self.position[1] += 1
    elif direction == 'n':
      self.position[1] -= 1
    elif direction == 'e':
      self.position[0] += 1
    elif direction == 'w':
      self.position[0] -= 1
  
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
  
  def sense(self):
    self.send("sense")