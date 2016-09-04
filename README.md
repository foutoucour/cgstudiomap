[![Build Status](https://travis-ci.org/cgstudiomap/cgstudiomap.svg?branch=develop)](https://travis-ci.org/cgstudiomap/cgstudiomap)
[![Code Climate](https://codeclimate.com/github/cgstudiomap/cgstudiomap/badges/gpa.svg)](https://codeclimate.com/github/cgstudiomap/cgstudiomap)
[![Codacy Badge](https://www.codacy.com/project/badge/204f84f106464aca9541acc97213c31a)](https://www.codacy.com/app/kender-jr/cgstudiomap)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/b7db6265f65443b0b61e21c5c0b257fe/badge.svg)](https://www.quantifiedcode.com/app/project/b7db6265f65443b0b61e21c5c0b257fe)


# cgstudiomap

## How to use

cgstudiomap is now under docker and docker-compose.

Requirement to run the project:
* [docker](https://docs.docker.com/engine/installation/) version 1.11.1
* [docker-compose](https://docs.docker.com/compose/install/) version 1.6.2

The setup is based on `services.yml`, where all the bases of each services are defined.
The setup of the steps are defined in inheriting yml files.

## Environments
Following the different environments for the instance.

### Development
To develop cgstudiomap, you will need to copy the `docker-compose.sample` to `docker-compose.yml`
and run once

    docker-compose up

From there, you should use odoo interface to create the database to finish the setup.

That will build all the context to develop into the docker. To stop the running instance:

    ctrl+c

After that you will need to edit the `docker-compose.yml` file to reflect the modification you did:
Change the command to run the update of the module you changed. For example, if you worked on frontedn_about module:

    /opt/cgstudiomap/parts/odoo/openerp-server -c /opt/cgstudiomap/etc/odoo.cfg --workers=0 --unaccent -u frontend_about

Then run

    docker-compose up

#### Development FAQ

1. When I run docker-compose up I see this error message.

        ERROR:
            Can't find a suitable configuration file in this directory or any parent. Are you in the right directory?
            Supported filenames: docker-compose.yml, docker-compose.yaml
    That means you didn't copy the docker-compose.sample file to docker-compose.yml

2. When I run docker-compose up, I see this error message about Invalid Bind:

        ERROR: Invalid bind mount spec "": Invalid volume destination path: '[' mount path must be absolute.

    You should run _docker-compose down_ to stop previous instances.

3. Where are stored the databases?

    The databases of the instances are stored at _~/.containers/cgstudiomap-pgsql-9.4_.

    Path is defined in _services.yml_.

### Test
The tests on github are setup in `.travis.yml`.

To run the tests locally, run:

    docker-compose -f docker-compose.test.yml up


### Production
Definition of the production environment is done in the file `docker-compose.prod.yml`.

To update the code in production, run:

    docker-compose -f docker-compose.prod.yml up


## Instance Definitions

The instance is defined in the `Dockerfile`.

Most likely, the definition itself won't have to be change more than occasionally as
system requirements and python requirements are defined in separate files.

* System requirements are defined in `requirements_apt.txt`.
* Python requirements are defined in `requirement_pip.txt`.

    _Note that the requirement of odoo itself are extracted from the requirements file of the odoo repo.
    No need to take care of them._


## Resources:
* [code quality](https://codeclimate.com/github/cgstudiomap/cgstudiomap)
* [codacy](https://www.codacy.com/app/kender-jr/cgstudiomap/dashboard)
* [backlog](https://huboard.com/cgstudiomap/cgstudiomap) 
* [Qualified Code](https://www.quantifiedcode.com/app/project/b7db6265f65443b0b61e21c5c0b257fe)
