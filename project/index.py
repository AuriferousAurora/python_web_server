# from services import reddit_auth
# response = reddit_auth()

# first party imports
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import os
import time

# local imports
from constants import DEV_HOST, PROD_HOST, TEMPLATE_DIR
from routes import routes

from response.request_handler import BadRequestHandler, StaticHandler, TemplateHandler

host_name = DEV_HOST
server_port = 4242

class Server(BaseHTTPRequestHandler):
  def _handle_http(self, handler):
    status_code = handler.get_status()

    self.send_response(status_code)

    if status_code is 200:
      content = handler.get_contents()
      self.send_header('Content-type', handler.get_content_type())
    else:
      content = "404 Not Found"

    self.end_headers()

    if isinstance(content, (bytes, bytearray) ):
      return content

    return bytes(content, "utf-8")
  
  def _respond(self, opts):
    response = self._handle_http(opts["handler"])
    self.wfile.write(response)
  
  def do_HEAD(self):
    return

  def do_GET(self):
    split_path = os.path.splitext(self.path)
    request_extension = split_path[1]
    if request_extension is "" or request_extension is ".html":
      if self.path in routes:
        handler = TemplateHandler()
        handler.find(routes[self.path])
      else:
        handler = BadRequestHandler()
    elif request_extension is ".py":
      handler = BadRequestHandler()
    else:
      handler = StaticHandler()
      handler.find(self.path)

    self._respond({
      "handler": handler
    })

  def do_POST(self):
    return

if __name__ == '__main__':
  server = HTTPServer((host_name, server_port), Server)
  print('Server started at http://%s:%s' % (host_name, server_port))
  
  try:
    server.serve_forever()
  except KeyboardInterrupt:
    pass

  server.server_close()
  print('Server stopped.')
