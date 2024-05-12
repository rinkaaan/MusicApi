source ~/startup.sh
WORKPLACE="$HOME/workplace/Music"

WORKSPACE="$WORKPLACE/MusicApi"
(
  cd "$WORKSPACE"
  rsync-project Music
  ssh root@hetzner "source ~/startup.sh && cd ~/workplace/Music/MusicApi && py-install"
)
