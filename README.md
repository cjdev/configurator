Configurator is a simple configuration assembler for managing configuration across environments. 

## Features:

  - yaml as configuration language
  - flatfile database for easy tracking of configuration changes
  - environmental mixins for extensible configuration (e.g: staging extends dev)

## How it works

Configurator takes a directory structure defining configurations for named environments Given a directory structure like:

    example
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
Providing a base environment, or providing environment specific overrides are both optional, if neither are included the directory will show up as an empty object.
Directory structure is completely free-form to allow for any shape of configuration and organization.

If we ask for the configuration for staging we end up with a structure like:

```python

{'example': 
  {
    'version': '0.0.1',
    'db': {'debug': True,
           'host': 'affordable-server.example.com',
           'port': 1337},
    'web': {'host': 'dev.example.com',
            'mount': '/app'}
  }
}

```

Check out the example contents for more information

## Installation
To get up and running:

    pip install -r requirements.txt

To try it out:

    python configurator.py

## Usage

Todo
