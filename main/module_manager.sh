#!/usr/bin/env bash
# Name of the database to use
database=$1;
# mode should be -i for initialize and -u for update
mode=$2;
# list of modules to act on, separated by ','
modules=$3;
echo "/opt/cgstudiomap/parts/odoo/openerp-server -c /opt/cgstudiomap/etc/odoo.cfg --stop-after-init --workers=0 -d $database $mode $modules"
docker-compose run cgstudiomap /opt/cgstudiomap/parts/odoo/openerp-server -c /opt/cgstudiomap/etc/odoo.cfg --stop-after-init --workers=0 -d $database $mode $modules
