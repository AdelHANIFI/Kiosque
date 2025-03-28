#!/bin/bash

sleep 30
export DISPLAY=:0.0
export XAUTHORITY=/home/mosqueePau/.Xauthority
git config --global --add safe.directory "/home/mosqueePau/Desktop/Kiosque"
git config --global credential.helper store 

#GIT_REPO="https://ghp-PRyB9ZQidR7TWYkivZjHe7hnroxz1A1HUrQo@github.com/AdelHANIFI/Kiosque.git"


cd /home/mosqueePau/Desktop/Kiosque 



. myenv/bin/activate

git add .
git commit -m "mise à jour automatique $(date '+%Y-%m6%d %H:%M:%S')"

git push origin main

git pull origin main

sudo pkill -f main.py 
python main.py &

