from flask import Flask, request
from flask.views import MethodView
from core import Configurator


class ConfigView(MethodView):
    def __init__(self, format, directory, *configs):
        self.directory = directory
        self.configs = configs
        self.format = format

    def __get_request_configs(self):
        config_arg = request.args.get('config')

        if config_arg is None:
            return self.configs
        else:
            return config_arg.split(",")

    def __get_request_format(self):
        return request.headers.get('accept', "/" + self.format).split("/")[1]

    def __serialize(self, config):
        node = request.args.get('node')

        if node is None:
            return config.serialize()
        else:
            cursor = config.config
            for part in node.split('.'):
                cursor = cursor[part]
            return config.serialize(config=cursor)

    def get(self):
        configs = self.__get_request_configs()
        request_format = self.__get_request_format()
        config = Configurator(request_format, self.directory, *configs)
        return self.__serialize(config)


class WebApi:
    def __init__(self, default_format, directory, *default_configs):
        app = Flask("configurator")
        view = ConfigView.as_view("config", default_format,
                                  directory, *default_configs)
        app.add_url_rule("/", view_func=view)

        self.app = app

    def run(self, **kwargs):
        self.app.run(**kwargs)
