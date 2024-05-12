WORKPLACE="$HOME/workplace/Music"

(
  cd "$WORKPLACE/MusicModels"
  pip install .
  rm -rf build
)
