#to load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
fi

#default to port 5000 if PORT is not set in the environment
PORT=${PORT:-5000}

#to start the API endpoint
python3 App.py

#to run Request_send.py file.
locust -f Request_send.py --host=http://localhost:$PORT/v1

#to run process.py
python3 process.py

#to run monitor.py
python3 monitor.py

#to run locust with defined file and image folder:
export CSV_FILE="{CSV_FILE}" && export IMAGES_FOLDER="{IMAGES_FOLDER}" && locust -f Request_send.py --headless  --host=http://localhost:$PORT/v1 --users 1 --spawn-rate 1'