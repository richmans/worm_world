from time import sleep
from threading import Thread
import random
import os
import glob

from worm_controller import WormController
from worm import Worm
from world import World
from visualization import Visualization
from random_controller import RandomController
from greedy_controller import GreedyController

class Simulation:
  width = 100
  height = 100
  amount_food = 100
  num_worms = 10
  start_health = 100
  controllers = []
  
  def spawn_worms(self):
    random.seed()
    for i in range(0, self.num_worms):
      x =  random.randrange(1, self.width - 1)
      y =  random.randrange(1, self.height - 1)
      position = [x, y]
      sim_worm = Worm(i, "", self.sim_world, self.start_health, position)
      self.sim_world.add_worm(sim_worm)
      #TODO controller balancing needs to be implemented every generation
      self.controllers[0].control_worm(sim_worm)
    print("Woo! %d new worms were born" % len(self.sim_world.worms))
      
  def start_controller(self):
    self.controllers.append(GreedyController())

  def start(self):    
    self.start_controller();
    self.sim_world = World(self.width, self.height, self.amount_food)
    self.spawn_worms()
    self.sim_visualization = Visualization(self.sim_world)
    self.thread = Thread(None, self.run_world, "World").start()
    #this will block
    self.sim_visualization.run()

  
  def run_world(self):  
    while True:
      #sleep(0.1)
      self.sim_world.sense()
      self.controllers[0].execute_moves()
      if len(self.sim_world.worms) == 0: break
    print("WormWorld just became very silent")
      
Simulation().start()