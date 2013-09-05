Configurator is a simple configuration assembler for managing configuration across environments.

## Features:

  - yaml as configuration language
  - flatfile database for easy tracking of configuration changes
  - environmental mixins for extensible configuration (e.g: staging extends dev)
  - simple validation against null configuration entries

## How it works

Configurator takes a directory structure defining configurations for named environments.
Given a directory structure like:

    configs
    |-- base.yml
    |-- db
    |   |-- base.yml
    |   |-- prod.yml
    |   `-- staging.yml
    `-- web
        |-- base.yml
        `-- prod.yml

We can see configurations defined for environments named `base`, `prod`, and `staging`.

When the special environment `base.yml` is found it provides default configuration for other environments to extend.
Providing a base environment or providing environment specific overrides are optional; if neither are included the directory will show up as an empty object.
Directory structure is completely free-form to allow for any shape of configuration and organization.

If we ask for the configuration for staging we end up with a structure like:

```yaml

db:
  debug: true
  host: affordable-server.example.com
  port: 1337
version: 0.0.1
web:
  host: dev.example.com
  mount: /app

```

## Installation

The recommended way to use configuration is to get a hold of one of the [pre-compiled linux binaries](https://github.com/cjdev/configurator/releases).

Currently tested on Debian 32 (i686) and 64 (x86_64) systems

### Manual installation

    pip install -r requirements.txt
    python configurator.py
    alias configurator="python $PWD/configurator.py"

## Usage

Configurator can either be used as a command line utility or as a web service.

#### web

    configurator --serve -p 12345
    # * Running on http://0.0.0.0:12345/

    curl localhost:12345?env=prod
    # get production environment config

    curl -H "Accept: application/json" localhost:12345 
    # get the default configs as json

#### cli

    configurator
    # runs configurator with your default configuration (cwd, yaml, base)

    configurator -h
    # displays help text

    configurator --format json --directory example/configs -e prod | python -m json.tool
    # pretty prints the prod configs from the example/configs directory as json

Check out the [examples](https://github.com/cjdev/configurator/tree/master/example) for an idea of how to get started managing your own configs.

### Configuration File

If a `~/.configurator` yaml document is found it will be loaded for default configuration.

Any configuration available from the command line is supported here.

## Questions?

File an issue or get in touch!
