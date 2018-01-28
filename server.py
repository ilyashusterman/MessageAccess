import os
import tornado.ioloop
import tornado.web
from common.persistence_utils import get_message_content

TEMPLATES = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                         'templates'))


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('{}/{}'.format(TEMPLATES, 'index.html'))

    def post(self):
        message_id = (self.get_body_argument("message_id",
                                             default=None,
                                             strip=False))
        self.write(get_message_content(message_id))


def make_app():
    handlers = [
        (r'/', MainHandler),
    ]
    return tornado.web.Application(handlers)


if __name__ == '__main__':
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()
