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
from generation import Generation

class Simulation:
  width = 100
  height = 100
  amount_food = 100
  num_worms = 10
  start_health = 100
  smell_range = 10
  controllers = []
  finished = False
  sim_world = None
  def assign_controllers(self, generation):
    for worm in generation.worms:
      self.controllers[0].control_worm(worm)
    
  def stop(self):
    self.sim_world.stop()
    
  def start(self):    
    self.controllers.append(GreedyController())
    self.sim_visualization = Visualization(self)
    self.thread = Thread(None, self.run, "World").start()
    # this will block until self.finished == True
    self.sim_visualization.run()

  def initialize_generation(self):
    # a new world
    self.sim_world = World(self.width, self.height, self.amount_food)
    # a generation to live in it
    self.sim_generation = Generation(self.num_worms, self.sim_world, self.start_health, self.smell_range)
    # some controllers that control the worms
    self.assign_controllers(self.sim_generation)
    
  def run(self):
    # TODO implement generation iteration
    self.initialize_generation()
    self.run_world()
    print("Bye")
    self.finished = True
  
  def run_world(self):  
    while True:
      try:
        sleep(0.1)
        self.sim_world.step()
      except:
        print("ERRORRRR")
      if self.sim_world.alive_count == 0: break
    print("WormWorld just became very silent")
      
Simulation().start()