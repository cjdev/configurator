from os import path, walk, getcwd
from fnmatch import fnmatch

def find_files_by_names(directory, names):
    """ Walks a directory structure returning filepaths named by provided names """
    files = []
    for rootpath, dirs, filenames in walk(directory):
        filenames = map(lambda f: path.join(rootpath, f), names)
        files += filter(lambda f: path.isfile(f), filenames)
    return files

def with_exts(filename, exts):
    return map(lambda ext: "{0}.{1}".format(filename, ext), exts)

def find_environment_configs(*envs):
    filenames = with_exts("defaults", ["yml", "yaml"])
    for env in envs:
        filenames += with_exts(env, ["yml", "yaml"])
    return find_files_by_names(getcwd(), filenames)

if __name__ == "__main__":
    print "Loading up hyper kernels..."
    print(find_environment_configs("prod", "staging"))
    pass
