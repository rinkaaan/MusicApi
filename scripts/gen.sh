WORKPLACE="$HOME/workplace/Music"
WORKSPACE="$WORKPLACE/MusicApi"

(
  cd "$WORKSPACE/api"
  flask spec --output openapi.yaml > /dev/null
)
