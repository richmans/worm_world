import world
import visualization
import time
import threading
import worm
import random
import random_controller
import greedy_controller
class Simulation:
  width = 1000
  height = 1000
  amount_food = 1000
  num_worms = 1000
  start_health = 100
  controllers = []
  
  def spawn_worms(self):
    random.seed()
    for i in range(0, self.num_worms):
      x =  random.randrange(1, self.width - 1)
      y =  random.randrange(1, self.height - 1)
      position = [x, y]
      sim_worm = worm.Worm(i, "", self.sim_world, self.start_health, position)
      self.sim_world.add_worm(sim_worm)
      #TODO controller balancing needs to be implemented every generation
      self.controllers[0].control_worm(sim_worm)
    print("Woo! %d new worms were born" % len(self.sim_world.worms))
      
  def start_controller(self):
    self.controllers.append(greedy_controller.GreedyController())

  def start(self):    
    self.start_controller();
    self.sim_world = world.World(self.width, self.height, self.amount_food)
    self.spawn_worms()
    self.sim_visualization = visualization.Visualization(self.sim_world)
    self.thread = threading.Thread(None, self.run_world, "World").start()
    #this will block
    self.sim_visualization.run()

  
  def run_world(self):  
    while True:
      time.sleep(0.1)
      self.sim_world.simulate_step()
      if len(self.sim_world.worms) == 0: break
    print("WormWorld just became very silent")
      
Simulation().start()