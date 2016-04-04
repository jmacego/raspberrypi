from os import curdir, sep
from urlparse import urlparse, parse_qs
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sys

# Determine the mode: Test or Real 
Mode = "test" if len(sys.argv) > 1 and \
                 sys.argv[1] == "--test" else "real"
 
if Mode == "real":
  print "Mode: Real"
  init(SerialPort)
 
# Handlers for commands:
def handle_move(query):
  speed = float(query['speed'][0])
  print "move(%s)" % speed
  if Mode == "real":
    if speed < 0.0:
      backward(-speed)
    else:  
      forward(speed)
 
def handle_spin(query):
  speed = float(query['speed'][0])
  print "spin(%s)" % speed
  if Mode == "real":
    if speed < 0.0:
      turnLeft(-speed)
    else:
      turnRight(speed)
 
def handle_stop(query):
  print "stop()"
  if Mode == "real":
    stop()
 
# Custom HTTP request handler:
class ActionHandler(BaseHTTPRequestHandler):
   
  def do_GET(self):
    if self.path == "/":
      self.path = "/index.html"
 
    url = urlparse(self.path)
    action = url.path[1:]
    print "action: ", action
 
    query = parse_qs(url.query)
    print "query: ", query
 
    # Send back an image, if requested:
    if url.path == "/cam.gif":
      if (Mode == "real"):
        p = takePicture()
        savePicture(p,"cam.gif")
 
    if action == "move":
      handle_move(query)
    elif action == "spin":
      handle_spin(query)
    elif action == "stop":
      handle_stop(query) 
    else: # grab a file
      try:
        print "sending file: ", url.path
        f = open(curdir + sep + url.path) 
        self.send_response(200)
        if url.path.endswith('.html'):
          self.send_header('Content-type', 'text/html')
        elif url.path.endswith('.js'):
          self.send_header('Content-type', 'text/javascript')
        elif url.path.endswith('.gif'):
          self.send_header('Content-type', 'image/gif')
        self.end_headers()
        self.wfile.write(f.read()); f.close()
        return
      except IOError:
        self.send_error(404,'File Not Found: %s' % self.path)
 
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
    self.wfile.write('OK: ' + self.path) ;
 
try:
  server = HTTPServer(('0.0.0.0', 1701), ActionHandler)
  print 'Awaiting commands...'
  server.serve_forever()
except KeyboardInterrupt:
  print 'User terminated server'
  server.socket.close()
