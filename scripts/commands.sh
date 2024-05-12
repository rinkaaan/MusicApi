scp -r root@hetzner:/root/workplace/Music/MusicApi/sqlite.db /Volumes/workplace/Music/MusicApi/api/sqlite.db

scp -r /Volumes/workplace/Music/MusicApi/api/sqlite.db root@hetzner:/root/workplace/Music/MusicApi/sqlite.db
scp -r ~/cookies.txt root@hetzner:~/cookies.txt

ln -sf /Volumes/workplace/Music/MusicApi/sqlite.db /Volumes/workplace/Music/MusicApi/api/sqlite.db
