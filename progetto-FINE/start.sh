export FLASK_APP=app.py

gnome-terminal -e "flask run"
sleep 4
google-chrome "http://127.0.0.1:5000/"