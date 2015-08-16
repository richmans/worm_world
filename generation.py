import random
from worm import Worm
class Generation:
  def __init__(self, size, world, start_health, smell_range):
    self.world = world
    self.worms = []
    random.seed()
    for i in range(0, size):
      x =  random.randrange(1, world.width - 1)
      y =  random.randrange(1, world.height - 1)
      position = [x, y]
      sim_worm = Worm(i, "", world, start_health, position, smell_range)
      self.worms.append(sim_worm)
      world.add_worm(sim_worm)
    print("Woo! %d new worms were born" % len(self.worms))
  