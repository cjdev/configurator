#!/usr/bin/env python

from os import path, walk, getcwd
from copy import deepcopy
from argparse import ArgumentParser
import yaml
import json

YAML_FORMATS = ["yml", "yaml"]
BASE_CONFIG = "base"


def get_arg_parser():
    parser = ArgumentParser(description="Configurate your self!")

    parser.add_argument(
        "-d", "--directory",
        help="Directory containing configuration hierarchy",
        default=getcwd(),
        metavar="DIR"
        )

    parser.add_argument(
        "-e", "--environment",
        help="Load environment specific overrides",
        default=[],
        nargs="+",
        metavar="ENV"
        )

    parser.add_argument(
        "--format",
        help="Output Format",
        choices=["json", "yaml"],
        default="yaml"
        )

    parser.add_argument(
        "--strict",
        help="Disallow NULL values in configuration (default)",
        dest="strict",
        action="store_true"
        )

    parser.add_argument(
        "--not-strict",
        help="Allow NULL values in configuration",
        dest="strict",
        action="store_false"
        )

    parser.set_defaults(strict=True)

    return parser


def get_formatter(args):
    if args.format == "json":
        def json_dumper(obj):
            return json.dumps(obj, sort_keys=True)
        return json_dumper
    else:
        def yaml_dumper(obj):
            return yaml.dump(obj, default_flow_style=False)
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
    config = yaml.load(file(path, "r")) or {}
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
    args = get_arg_parser().parse_args()
    basedir = args.directory
    envs = args.environment
    paths = find_config_paths(basedir, *envs)
    configs = paths_to_configs(paths, basedir)
    config = merge_configs(configs)

    if args.strict:
        assert validate_structure(config), \
            "Configuration may not contain NULL values"

    print get_formatter(args)(config)
