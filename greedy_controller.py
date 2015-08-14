import random
class GreedyController:
  worms = {}
  def control_worm(self, worm):
    worm.controller = self
    self.worms[worm.id] = worm
    
  def handle_event(self, worm_id, command, data):
    if command == 'sense': self.handle_sense(worm_id, data)
  
  def determine_direction(self, sensors):
    food_sensors = sensors[0:4]
    wall_sensors = sensors[4:8]
    max_food = max(food_sensors)
    max_wall = max(wall_sensors)
    
    if max_food > 0.1:
      direction = food_sensors.index(max_food)
    else:
      wrong_direction = wall_sensors.index(max_wall)
      if wrong_direction == 0:
        direction = 2
      else:
        direction = 0
    return direction
    
  def handle_sense(self, worm_id, data):
    directions = ['n','e', 's', 'w']
    worm = self.worms[worm_id]
    if worm == None: return
    direction = self.determine_direction(data)
    direction_character = directions[direction]
    worm.move(direction_character)
  
  