import os

class MockFile():
  def read(self):
    return False

class RequestHandler():
  def __init__(self):
    self.content_type = ""
    self.contents = MockFile()

  def get_contents(self):
    return self.contents.read()
  
  def read(self):
    return self.contents

  def set_status(self, status):
    self.status = status

  def get_status(self):
    return self.status

  def get_content_type(self):
    return self.content_type

  def get_type(self):
    return "static"

class TemplateHandler(RequestHandler):
  def __init__(self):
    super().__init__()
    self.content_type = "text/html"

  def find(self, route_data):
    try:
      template_file = open("templates/{}".format(route_data["template"]))
      self.contents = template_file
      self.set_status(200)
      
      return True
    except:
      self.set_status(404)
      
      return False

class StaticHandler(RequestHandler):
  def __init__(self):
    super().__init__()
    self.filetypes = {
      ".js" : "text/javascript",
      ".css" : "text/css",
      ".jpg" : "image/jpeg",
      ".png" : "image/png",
      "notfound" : "text/plain"
    }

  def find(self, file_path):
    split_path = os.path.splitext(file_path)
    extension = split_path[1]

    # todo: include logic to prevent access to other directories via .. command
    try: 
      if extension in (".jpg", ".jpeg", ".png"):
        self.contents = open("public{}".format(file_path), 'rb')
      else:
        self.contents = open("public{}".format(file_path), 'r')

      self.set_content_type(extension)
      self.set_status(200)
      
      return True
    except:
      self.set_content_type("notfound")
      self.set_status(404)

      return False

  def set_content_type(self, ext):
      self.content_type = self.filetypes[ext]

class BadRequestHandler(RequestHandler):
  def __init__(self):
    super().__init__()
    self.content_type = "text/plain"
    self.set_status(404)
