#(cd api && flask run --host=0.0.0.0 --port $PORT)
# For running locally
#(cd .. && PYTHONPATH=. python -u api/app.py)
# For pm2
#(PYTHONPATH=. python -u api/app.py)
#(cd .. && export PORT=34201 PYTHONPATH=. && gunicorn -w 1 'api.app:app' -b 0.0.0.0:$PORT)
#(export PYTHONPATH=. && PYTHONUNBUFFERED=TRUE gunicorn -w 1 'api.app:app' -b 0.0.0.0:$PORT)
(export PYTHONPATH=. && PYTHONUNBUFFERED=TRUE flask --app api.app run --host=0.0.0.0 --port $PORT --no-reload)

