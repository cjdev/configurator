Configurator is a simple configuration assembler for managing configuration across environments.


## Features:

  - yaml as configuration language
  - yaml or json as output formats
  - flatfile database for easy tracking of configuration changes
  - mixins for extensible configuration
  - http api for serving configs over a network

## How it works

Configurator takes a directory structure defining configurations for named environments.
Given a directory structure like:

    configs
    |-- defaults.yml
    |-- db
    |   |-- defaults.yml
    |   |-- prod.yml
    |   `-- staging.yml
    `-- web
        |-- base.yml
        `-- prod.yml

We can see configs named `defaults`, `prod`, and `staging`.

When the special config `base.yml` is found it provides default configuration for other configs to extend.
Providing a base config or config mixins are optional.
Directory structure is completely free-form to allow for any shape of configuration and organization.

If we ask for the configuration for staging we end up with a structure like:

```yaml

version: 0.0.1
db:
  hosts:
    - affordable-server.example.com
  vars:
    port: 1337
    debug: true
web:
  hosts:
    - dev.example.com
  vars:
    mount: /app

```

## Installation

The recommended way to use configurator is to get a hold of one of the [pre-compiled linux binaries](https://github.com/cjdev/configurator/releases).

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

    curl 'localhost:12345?config=prod&node=db.host'
    # get the db host from the production config

    curl -H "Accept: application/json" localhost:12345
    # get the default configs as json

#### cli

    configurator
    # runs configurator with your default configuration (cwd, yaml, base)

    configurator -h
    # displays help text

    configurator --format json --directory example/configs -c prod | python -m json.tool
    # pretty prints the prod configs from the example/configs directory as json


### Uses

Check out the [examples](https://github.com/cjdev/configurator/tree/master/example) for an idea of how to get started managing your own configs, including how to use configurator as a simple backend for ansible configuration.

### Configurator configuration

If a `~/.configurator` yaml document is found it will be loaded for default configuration.

Any configuration available from the command line is supported here.

## Questions?

File an issue or get in touch!
