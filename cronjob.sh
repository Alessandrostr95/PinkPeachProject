#!/usr/bin/env sh

# -- get latest version
cd /home/tvstudents/PinkPeachProject
git pull origin main

# -- download latest data
cd src
# ---- for bachelor
python3 scraper.py bachelor -a -y 20-21
python3 scraper.py bachelor -a -y 21-22
# ---- for master
python3 scraper.py master -a -y 20-21
python3 scraper.py master -a -y 21-22

# -- generate latest version
cd ..
./generate.sh
