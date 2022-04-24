import sys

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from projectmanager.app import app
import projectmanager.router
from projectmanager.config import PORT, IS_DEBUG


if __name__ == '__main__':
    app.run(
        debug=IS_DEBUG,
        port=PORT
    )
    # if sys.argv[1] == 'flask':
    #     app.run(
    #         debug=IS_DEBUG,
    #         port=PORT
    #     )
    # elif sys.argv[1] == 'tornado':
    #     http_server = HTTPServer(WSGIContainer(app))
    #     http_server.listen(PORT)
    #     IOLoop.instance().start()
    # else:
    #     print('Please enter correct parameters!')
