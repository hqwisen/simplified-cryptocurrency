#!/usr/bin/env bash

MASTER_PORT=8000
RELAY_PORT_PRE=800
MASTER_SETTINGS="master.settings"
RELAY_SETTINGS="relay.settings"

master(){
    echo "Starting MasterNode on $MASTER_PORT"
    python manage.py runserver $MASTER_PORT --settings $MASTER_SETTINGS
}

relay(){
    echo "Starting RelayNode on $RELAY_PORT_PRE$1"
    python manage.py runserver $RELAY_PORT_PRE$1 --settings $RELAY_SETTINGS
}

if [ "$1" != "master" ] && [ "$1" != "relay" ]; then
    echo "Error: option must be 'master' or 'relay X'"
    exit 1
fi

if [ "$1" == "relay" ] && ! [[ "$2" =~ ^[0-9]+$ ]]; then
    echo "Error: '$2' is not a correct relay number"
    exit 1
fi

$1 $2