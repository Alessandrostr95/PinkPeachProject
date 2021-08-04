#!/usr/bin/env sh

# This script is used to generate the site.

export SITE_ROOT="./site/"
export SRC_ROOT="./src/"
export DATA_ROOT="./data/"
export TEMPLATES_ROOT="./templates/"
export ASSETS_ROOT="./assets/"

main() {
    # -- clean previous version
    rm -r $SITE_ROOT

    # -- create new version    
    mkdir $SITE_ROOT
    mkdir $SITE_ROOT/home
    mkdir $SITE_ROOT/triennale
    mkdir $SITE_ROOT/triennale/20-21
    mkdir $SITE_ROOT/magistrale
    mkdir $SITE_ROOT/magistrale/20-21

    cp -r $ASSETS_ROOT $SITE_ROOT
    
    python3 src/site_generator/home.py
    python3 src/site_generator/orari.py
    python3 src/site_generator/docenti.py
    # python3 src/site_generator/assets.py
}

# call main with all arguments passed from command line
main $@
