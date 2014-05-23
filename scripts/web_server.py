import cherrypy
import json
import os
from cherrypy.lib.static import serve_file



class Config(object):

    exposed = True

    def __init__(self, config_parser):
        self.config = config_parser

    @cherrypy.expose
    def image(self, blah):
        print "handling image"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return serve_file(os.path.join(current_dir, 'raw.py'), content_type='text/text')

    def get_config(self):
        """ Return a config as a dictionary"""
        dict = {}
        for section in self.config.sections():
            for option in self.config.options(section):
                dict[section + '.' + option] = self.config.get(section, option)

        return dict

    def GET(self, id=None):
        if id == None:
            return json.dumps(self.get_config())
        else:
            return self.get_config()[id]    

class Image(object):

    exposed = True

    def __init__(self):
        pass

    def GET(self, id=None):
        print "handling image"
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return serve_file(os.path.join(current_dir, '/tmp/frame.jpg'), content_type='image/jpeg')

class Static:
    exposed = True

class Webserver(object):
    def __init__(self, config_parser):
        cherrypy.tree.mount(
            Config(config_parser), '/config',
            {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()} } )
        cherrypy.tree.mount(
            Image(), '/image',
            {'/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()} } )


        cherrypy.config.update({
                         'server.socket_port': 8081 
                        }) 

        cherrypy.engine.start()
        # cherrypy.engine.block()

if __name__ == '__main__':

    Webserver()
    cherrypy.engine.block()