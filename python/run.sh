 rm __pycache__/*
 pkill -f "cal2bitable"
 #gunicorn --bind 0.0.0.0:1323 cal2bitable:app --daemon
 gunicorn --bind 0.0.0.0:1323 cal2bitable:app
