from argparse import ArgumentParser
from os import path, getcwd


def get_defaults():
    defaults = {
        "strict": True,
        "directory": getcwd(),
        "format": "yaml",
        "configs": []
    }

    config_file = path.expanduser("~/.configurator")

    if path.isfile(config_file):
        with open(config_file) as f:
            user_config = yaml.load(f)

        defaults.update(user_config)
        return defaults
    else:
        return defaults


def get_arg_parser():
    parser = ArgumentParser(description="Configurate your self!")

    parser.add_argument(
        "-d", "--directory",
        help="Directory containing configuration hierarchy",
        metavar="DIR"
        )

    parser.add_argument(
        "-c", "--configs",
        help="Load specific configs",
        nargs="+",
        metavar="CONFIG"
        )

    parser.add_argument(
        "--format",
        help="Output Format",
        choices=["json", "yaml"],
        )

    parser.add_argument(
        "--strict",
        help="Validate values in configuration (default)",
        dest="strict",
        action="store_true"
        )

    parser.add_argument(
        "--not-strict",
        help="Don't validate values in configuration",
        dest="strict",
        action="store_false"
        )

    parser.add_argument(
        "-p", "--port",
        help="Port to start the configurator server on",
        default=5000,
        type=int,
        )

    parser.add_argument(
        "--serve",
        help="start a configurator server with the given settings",
        action="store_true",
        default=False
        )

    parser.set_defaults(**get_defaults())

    return parser


def parse_args():
    return get_arg_parser().parse_args()
