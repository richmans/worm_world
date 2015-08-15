import random
from worm_controller import WormController
class RandomController(WormController):
  def handle_sense(self, worm_id, data):
    directions = ['n','e', 's', 'w']
    worm = self.worms[worm_id]
    if worm == None: return
    direction = directions[random.randrange(0, 4)]
    worm.queue_move(direction)
  