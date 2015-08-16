import socket
from struct import *
from greedy_controller import GreedyController
class RemoteClient:
  # This class has a lot of code duplication from remote_controller because
  # i want it to be standalone
  port = 52192
  host = "127.0.0.1"
  verbs = {
    "HelloServer": 1,
    "HelloClient": 2,
    "Worm": 3,
    "Ok": 4,
    "Nok": 5,
    "Sense": 6,
    "Move": 7,
    "Kill": 8,
    "Bye": 9
  }
  verb_map = {v: k for k, v in verbs.items()}
  
  def __init__(self, name):
    self.name = name
    self.controller = GreedyController()
    self.finished = False
    
  def start(self):
    self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.conn.connect((self.host, self.port))
    self.receive()
  
  def send(self, verb_str, data=None):
    verb = self.verbs[verb_str]
    if data == None: data = b""
    length = len(data)
    message = pack("<BI", verb, length) + data
    self.conn.sendall(message)
  
  def recv(self, length):
    return self.conn.recv(length)
  
  def receive(self):
    while True:
      if self.finished: break
      verb = self.conn.recv(1)
      if not verb: break
      self.handle_message(verb)
    
  def handle_message(self, verb_bt):
    verb = unpack("B", verb_bt)[0]
    length_bt = self.recv(4)
    length = unpack("I", length_bt)[0]
    try:
      verb_str = self.verb_map[verb]
    except KeyError:
      verb_str = "Unknown %d" % verb
    if verb_str == "HelloServer":
      self.handle_hello()
    elif verb_str == "Worm":
      self.handle_worm()
    elif verb_str == "Sense":
      self.handle_sense()
    elif verb_str == "Kill":
      self.handle_kill()
    elif verb_str == "Ok":
      pass
    elif verb_str == "Bye":
      self.handle_bye()
    else:
      self.recv(length)
      print("Verb %s not implemented yet" % verb_str) 
  
  def handle_worm(self):
    data = self.recv(8)
    worm_id, dna_len = unpack("II", data)
    if dna_len > 0: 
      dna = self.recv(dna_len)
    print("Now controlling worm %d" % worm_id)
    self.send("Ok")
  
  def handle_kill(self):
    worm_id = unpack("<I", self.recv(4))[0]
    print("Worm %d got killed" % worm_id)
    
  def handle_hello(self):  
    print("Hello from the remote server")
    message = pack("B", len(self.name)) + self.name 
    self.send("HelloClient", message)
 
  def send_move(self, worm_id, direction):
    message = pack("<I", worm_id) + direction
    self.send("Move", message)
    
  def handle_sense(self):
    directions = ['n','e', 's', 'w']
    worm_id, num_senses = unpack("<IB", self.recv(5))
    senses_bt = self.recv(num_senses)
    senses = unpack("%dB" % num_senses, senses_bt)
    self.send("Ok")
    direction = self.controller.determine_direction(senses)
    direction_character = directions[direction]
    self.send_move(worm_id, direction_character)
  
  def handle_bye(self):
    print("Server said byebye, shutting down")
    self.finished = True
     
RemoteClient("Test client").start()