start /MIN cmd /C flask run 
timeout 4
start /MAX chrome "http://127.0.0.1:5000/"