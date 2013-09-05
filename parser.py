from os import path, walk
from copy import deepcopy
import yaml
import json

YAML_FORMATS = ["yml", "yaml"]
BASE_CONFIG = "base"


def json_dumper(obj):
    return json.dumps(obj, sort_keys=True)


def yaml_dumper(obj):
    return yaml.dump(obj, default_flow_style=False)


def get_formatter(format):
    if format == "json":
        return json_dumper
    else:
        return yaml_dumper


def validate_structure(d):
    for k, v in d.iteritems():
        if v is None:
            return False
        elif isinstance(v, dict):
            if not validate_structure(v):
                return False

    return True


def find_files_by_names(directory, names):
    """ walks a directory structure
        returning filepaths named by provided names """
    files = []
    for rootpath, dirs, filenames in walk(directory):
        filenames = map(lambda name: path.join(rootpath, name), names)
        files += filter(lambda f: path.isfile(f), filenames)
    return files


def filenames_by_exts(exts, *filenames):
    """ given ['json', 'ini'], configurator returns
        ['configurator.json', 'configurator.ini'] """
    fnames = []
    for filename in filenames:
        fnames += map(lambda ext: "{0}.{1}".format(filename, ext), exts)
    return fnames


def find_config_paths(directory, *environments):
    """ search for filenames matching the config format """
    filenames = filenames_by_exts(YAML_FORMATS, BASE_CONFIG, *environments)
    return find_files_by_names(directory, filenames)


def filepath_to_namespace(path, directory):
    """ given ./foo/bar/baz.yml returns ['foo', 'bar'] """
    return path[len(directory):].lstrip("/").split("/")[:-1]


def namespace_node(namespace, node):
    """ given ['a', 'b', 'c'], 23 returns {a: {b: {c: 23}}} """
    last = len(namespace) - 1
    obj = {}
    ref = obj
    for i, name in enumerate(namespace):
        if i == last:
            ref[name] = node
        else:
            ref[name] = {}
        ref = ref[name]
    return obj


def load_namespaced_yaml(path, directory):
    """ Loads a yaml document namespacing it by the directory structure
        relative to directory """
    config = yaml.load(file(path, "r")) or {}
    namespace = filepath_to_namespace(path, directory)
    if len(namespace) > 0:
        return namespace_node(namespace, config)
    else:
        return config


def paths_to_configs(paths, directory):
    return map(lambda path: load_namespaced_yaml(path, directory), paths)


def deep_merge(a, b):
    """ recursively merges dicts """
    # borrowed from
    # http://www.xormedia.com/recursively-merge-dictionaries-in-python/
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result


def merge_configs(configs):
    """ more like partial reduce deep_merge amirite """
    result = {}
    for config in configs:
        result = deep_merge(result, config)
    return result


def generate_config(directory, *envs):
    paths = find_config_paths(directory, *envs)
    configs = paths_to_configs(paths, directory)
    return merge_configs(configs)


class Configurator:
    def __init__(self, default_format, directory, *environments):
        self.default_format = default_format
        self.directory = directory
        self.environments = environments
        self.config = generate_config(directory, *environments)

    def validate(self):
        assert validate_structure(self.config), \
            "Configuration may not contain NULL values"

    def serialize(self, format=None):
        if format:
            formatter = get_formatter(format)
        else:
            formatter = get_formatter(self.default_format)
        return formatter(self.config)
