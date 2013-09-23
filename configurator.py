#!/usr/bin/env python
from configurator.args import parse_args
from configurator.core import Configurator
from configurator.web import WebApi


if __name__ == "__main__":
    args = parse_args()

    if args.serve:
        app = WebApi(args.format, args.directory, *args.configs)
        app.run(host="0.0.0.0", port=args.port)
    else:
        config = Configurator(args.format, args.directory, *args.configs)

        if args.strict:
            config.validate()

        print config.serialize()
