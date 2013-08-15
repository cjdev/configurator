from os import path, walk, getcwd
from copy import deepcopy
from yaml import load


YAML_FORMATS = ["yml", "yaml"]
BASE_CONFIG = "base"


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


def find_config_paths(basedir, *environments):
    """ search for filenames matching the config format """
    filenames = filenames_by_exts(YAML_FORMATS, BASE_CONFIG, *environments)
    return find_files_by_names(basedir, filenames)


def filepath_to_namespace(path, basedir):
    """ given ./foo/bar/baz.yml returns ['foo', 'bar'] """
    return path[len(basedir):].lstrip("/").split("/")[:-1]


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


def load_namespaced_yaml(path, basedir):
    """ Loads a yaml document namespacing it by the directory structure
        relative to basedir """
    config = load(file(path, 'r')) or {}
    namespace = filepath_to_namespace(path, basedir)
    if len(namespace) > 0:
        return namespace_node(namespace, config)
    else:
        return config


def paths_to_configs(paths, basedir):
    return map(lambda path: load_namespaced_yaml(path, basedir), paths)


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


if __name__ == "__main__":
    basedir = getcwd()
    paths = find_config_paths(basedir)
    configs = paths_to_configs(paths, basedir)
    config = merge_configs(configs)

    from pprint import pprint
    pprint(config)
