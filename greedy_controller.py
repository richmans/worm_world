import random
class GreedyController:
  worms = {}
  def control_worm(self, worm):
    worm.controller = self
    self.worms[worm.id] = worm
    
  def handle_event(self, worm_id, command, data):
    if command == 'sense': self.handle_sense(worm_id, data)
  
  def determine_direction(self, sensors):
    max_value = max(sensors)
    return sensors.index(max_value)
    
  def handle_sense(self, worm_id, data):
    directions = ['n','e', 's', 'w']
    worm = self.worms[worm_id]
    if worm == None: return
    direction = self.determine_direction(data[0:4])
    direction_character = directions[direction]
    #print("Worm %d sensing %s moving %s" % (worm.id, data, direction_character))
    worm.move(direction_character)
  
  