import sys

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

# 因为考虑到import的不一致 如果install-e之后变成from filemanager import app了怎么办
# 所以先installl试试
# 第二天又想了一下,install是一个不可逆的操作，不如先直接这样试一下可不可以，如果不可以再说呗

from filemanager.app import app
import filemanager.router
from filemanager.config import PORT,IS_DEBUG

if __name__ == '__main__':
    app.run(
        debug=IS_DEBUG,
        port=PORT
    )