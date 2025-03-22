cd /home/mosqueePau/Desktop/Kiosque 

. myenv/bin/activate

git add .
git commit -m "mise à jour automatique $(date '+%Y-%m6%d %H:%M:%S')"

git push origin main

git pull origin main

sudo pkill -f main.py 
python main.py &

