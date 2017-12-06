#!/usr/bin/env bash

MASTER_PORT=8000
RELAY_PORT=8001
MASTER_SETTINGS="master.settings"
RELAY_SETTINGS="relay.settings"

master(){
    echo "Starting MasterNode on $MASTER_PORT"
    python manage.py runserver $MASTER_PORT --settings $MASTER_SETTINGS
}

relay(){
    echo "Starting RelayNode on $RELAY_PORT"
    python manage.py runserver $RELAY_PORT --settings $RELAY_SETTINGS
}

$1