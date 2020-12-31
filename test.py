import aiml
import os
import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
# Create the kernel and learn AIML files
kernel = aiml.Kernel()
#kernel.learn("std-startup.xml")
#'startup.xml file consist of all the information about AIML files
#aiml file consist information about  input and responce.
kernel.learn('startup.xml')
kernel.respond("load aiml b")

define('port', default=3999, help='run on the given port', type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
            (r'/chat', ChatHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            debug=True,
        )

        # conn = pymongo.Connection('localhost', 12345)
        # self.db = conn['demo']
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

    def post(self):

        result = {
            'is_success': True,
            'message': '123'
        }

        respon_json = tornado.escape.json_encode(result)
        self.write(str(respon_json))

    def put(self):
        respon_json = tornado.escape.json_encode("{'name':'qixiao','age':123}")
        self.write(respon_json)


class ChatHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('chat.html')

    def post(self):
        try:
            message = self.get_argument('msg', None)

            print(str(message))

            result = {
                'is_success': True,
                'message': str(kernel.respond(message))
            }

            print(str(result))

            respon_json = tornado.escape.json_encode(result)

            self.write(respon_json)

        except Exception, ex:
            repr(ex)
            print(str(ex))

            result = {
                'is_success': False,
                'message': ''
            }

            self.write(str(result))


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    print('HTTP server starting ...')
    main()

# Press CTRL-C to break this loop
#while True:
#    print kernel.respond(raw_input("Enter your message >> "))
