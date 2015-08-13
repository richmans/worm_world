import random
class RandomController:
  worms = {}
  def control_worm(self, worm):
    worm.controller = self
    self.worms[worm.id] = worm
    
  def handle_event(self, worm_id, command, data):
    if command == 'sense': self.handle_sense(worm_id, data)
  
  def handle_sense(self, worm_id, data):
    directions = ['n','s', 'w', 'e']
    worm = self.worms[worm_id]
    if worm == None: return
    direction = directions[random.randrange(0, 4)]
    worm.move(direction)