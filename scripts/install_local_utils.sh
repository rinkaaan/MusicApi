WORKPLACE="$HOME/workplace/Music"

(
  cd "$WORKPLACE/PythonUtils"
  pip install .
  rm -rf build
)
