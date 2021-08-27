#!/usr/bin/env sh

# This script is used to generate the site.

export SITE_ROOT="./site/"
export SRC_ROOT="./src/"
export DATA_ROOT="./data/"
export TEMPLATES_ROOT="./templates/"
export ASSETS_ROOT="./assets/"

main() {
    # -- clean previous version (?)
    # rm -r $SITE_ROOT

    # -- create new version    
    python3 src/site_generator/home.py
    python3 src/site_generator/contributors.py
    python3 src/site_generator/orari.py
    python3 src/site_generator/docenti.py
    python3 src/site_generator/corsi.py
    python3 src/site_generator/lista-corsi.py
    python3 src/site_generator/esami.py
    python3 src/site_generator/lauree.py
}

# call main with all arguments passed from command line
main $@
