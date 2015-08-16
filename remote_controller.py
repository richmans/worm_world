import socket
from threading import Thread
from struct import *
from worm_controller import WormController
class RemoteController(WormController):
  port = 52192
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
  
  def __init__(self):
    self.wait_for_connection()
    
  def wait_for_connection(self):
    print("Waiting for remote controller to connect")
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.bind(("0.0.0.0", self.port))
    self.sock.listen(1)
    self.handle_connection(self.sock)
    
  def handle_connection(self, sock):
    self.conn, addr = sock.accept()
    print("Remote Controller Connection from %s" % addr[0])
    self.thread = Thread(None, self.receive, "RemoteController").start()
    self.send("HelloServer")
  
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
      verb = self.conn.recv(1)
      if not verb: break
      self.handle_message(verb)
      
  def stop(self):
    self.send("Bye")
    self.sock.close()
    
  def handle_message(self, verb_bt):
    verb = unpack("B", verb_bt)[0]
    length_bt = self.conn.recv(4)
    length = unpack("I", length_bt)[0]
    try:
      verb_str = self.verb_map[verb]
    except KeyError:
      verb_str = "Unknown %d" % verb
    if verb_str == "HelloClient":
      self.handle_hello()
    elif verb_str == "Ok":
      pass
    elif verb_str == "Move":
      self.handle_move()
    else:
      self.recv(length)
      print("Verb %s not implemented yet" % verb_str)
  
  def handle_hello(self):
    data = self.recv(1)
    name_length = unpack("B", data)[0]
    name = self.recv(name_length)
    print("Hello from the remote controller " + name)
    
  def control_worm(self, worm):
    worm.controller = self
    self.worms[worm.id] = worm
    message = pack("II", worm.id, len(worm.dna))
    self.send("Worm", message)
    
  def handle_event(self, worm_id, command, data):
    if command == 'sense': self.handle_sense(worm_id, data)
    if command == 'kill' : self.handle_kill(worm_id)
  
  def handle_kill(self, worm_id):
    message = pack("<I", worm_id)
    self.send("Kill", message)
  
  def handle_move(self):
    worm_id = unpack("<I", self.recv(4))[0]
    direction = self.recv(1)
    worm = self.worms[worm_id]
    if worm == None: return
    worm.queue_move(direction)
    self.send("Ok")
    
      
  def handle_sense(self, worm_id, data):
    message = pack("IB%dB" % len(data), worm_id, len(data), *data)
    self.send("Sense", message)
  