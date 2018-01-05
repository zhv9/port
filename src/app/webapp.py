from flask import Flask, render_template
from flask_restful import reqparse, abort, Api, Resource, request
from src.app.api import (io_api, serial_api)
import threading


class WebApp(object):
    app = Flask(__name__,
                static_folder="./dist/static",
                template_folder="./dist")
    my_api = Api(app)

    def __init__(self):
        # threading.Thread.__init__(self)
        pass

    def init_api(self):
        io_api.init_api(self.my_api)
        serial_api.init_api(self.my_api)

    def get_app(self):
        return self.app

    def set_app(self, my_app):
        self.app = my_app

    def run(self):
        self.app.run(debug=True)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path):
        return render_template("index.html")


if __name__ == '__main__':
    my_web_app = WebApp()
    my_web_app.init_api()
    my_web_app.run()
