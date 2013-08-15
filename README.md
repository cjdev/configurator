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

The recommended way to use configuration is to get a hold of one of the pre-compiled linux binaries.
Currently tested on Debian 32 and 64bit systems

### Manual installation

    pip install -r requirements.txt
    python configurator.py

## Usage

If you have the binary distribution simply include it somewhere on your path and have fun.

    configurator -h
    # displays help text

    configurator --format json --directory example/configs -e prod | python -m json.tool
    # pretty prints the prod configs from the example/configs directory as json

    configurator
    # runs configurator with your default configuration (cwd, yaml, base)

    configurator -d example/configs -e null
    # blows up because null environment contains a null value

    configurator -d example/configs -e null --not-strict
    # allows null values


### Configuration File

If a `~/.configurator` yaml document is found it will be loaded for default configuration.

Any configuration available from the command line is supported here.

## Questions?

File an issue or get in touch!
