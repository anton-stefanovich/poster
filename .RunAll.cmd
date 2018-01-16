start python PosterMain.py --type=auto --destination=twitter --repeat=3 --delay=10000
timeout 60

start python PosterMain.py --type=auto --destination=facebook --repeat=3 --delay=10000
timeout 60

start python PosterMain.py --type=home --destination=facebook --repeat=3 --delay=10000
timeout 120

start python PosterMain.py --type=home --destination=twitter --repeat=10 --delay=4000
exit