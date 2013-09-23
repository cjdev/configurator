from flask import Flask, request
from flask.views import MethodView
from core import Configurator


class ConfigView(MethodView):
    def __init__(self, format, directory, *envs):
        self.directory = directory
        self.envs = envs
        self.format = format

    def __get_request_envs(self):
        env_arg = request.args.get('config')

        if env_arg is None:
            return self.envs
        else:
            return env_arg.split(",")

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
        environments = self.__get_request_envs()
        request_format = self.__get_request_format()
        config = Configurator(request_format, self.directory, *environments)
        return self.__serialize(config)


class WebApi:
    def __init__(self, default_format, directory, *default_envs):
        app = Flask("configurator")
        view = ConfigView.as_view("config", default_format,
                                  directory, *default_envs)
        app.add_url_rule("/", view_func=view)

        self.app = app

    def run(self, **kwargs):
        self.app.run(**kwargs)
