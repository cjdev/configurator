from os import path, walk, getcwd
from copy import deepcopy
from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def find_files_by_names(directory, names):
    """ Walks a directory structure returning filepaths named by provided names """
    files = []
    for rootpath, dirs, filenames in walk(directory):
        filenames = [path.join(rootpath, name) for name in names]
        files += filter(lambda f: path.isfile(f), filenames)
    return files

def with_exts(filename, exts):
    return ["{0}.{1}".format(filename, ext) for ext in exts]

def find_configs_paths(*envs):
    yamls = ["yml", "yaml"]
    filenames = with_exts("defaults", yamls)
    for env in envs:
        filenames += with_exts(env, yamls)
    return find_files_by_names('.', filenames)

def filepath_to_namespace(path, basedir="."):
    return path[len(basedir):].lstrip("/").split("/")[:-1]

def load_namespaced_yaml(path, basedir="."):
    """ Loads a yaml document namespacing it by the directory structure
        relative to basedir """
    config = load(file(path, 'r'))
    if config is None:
        config = {}
    namespace = filepath_to_namespace(path, basedir)
    if len(namespace) > 0:
        obj = {}
        current = obj
        for index, part in enumerate(namespace):
            if index + 1 == len(namespace):
                current[part] = config
            else:
                current[part] = {}
            current = current[part]
        return obj
    else:
        return config

def deep_merge(a, b):
    """ recursively merges dict's
        borrowed from: http://www.xormedia.com/recursively-merge-dictionaries-in-python/ """
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = deep_merge(result[k], v)
        else:
            result[k] = deepcopy(v)
    return result

def paths_to_configs(paths):
    return [load_namespaced_yaml(path) for path in paths]

def merge_configs(configs):
    result = {}
    for config in configs:
        result = deep_merge(result, config)
    return result

if __name__ == "__main__":
    print("Loading up hyper kernels...")
    paths = find_configs_paths()
    configs = paths_to_configs(paths)
    print(merge_configs(configs))
