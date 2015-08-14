class WormController:
  worms = {}
  moves = {}
  
  def control_worm(self, worm):
    worm.controller = self
    self.worms[worm.id] = worm
    
  def handle_event(self, worm_id, command, data):
    if command == 'sense': self.handle_sense(worm_id, data)
    if command == 'kill' : self.handle_kill(worm_id)
  
  def handle_kill(self, worm_id):
    pass
    
  def handle_sense(self, worm_id, data):
    pass
  
  def execute_moves(self):
    for worm_id in self.worms:
      worm = self.worms[worm_id]
      if not worm.alive: continue
      worm.move(self.moves[worm_id])