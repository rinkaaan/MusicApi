source ~/startup.sh
WORKPLACE="$HOME/workplace/Music"

WORKSPACE="$WORKPLACE/MusicApi"
(
  cd "$WORKSPACE"
  rsync-project Music
  ssh root@hetzner "pm2 restart api-media"
)
