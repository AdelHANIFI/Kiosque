#!/bin/bash

sleep 30
export DISPLAY=:0.0
export XAUTHORITY=/home/mosqueePau/.Xauthority


cd /home/mosqueePau/Desktop/Kiosque 

git remote set-url origin git@github.com:AdelHANIFI/Kiosque.git

. myenv/bin/activate

git add .
git commit -m "mise à jour automatique $(date '+%Y-%m6%d %H:%M:%S')"

git push origin main

git pull origin main

sudo pkill -f main.py 
python main.py &

