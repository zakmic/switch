#!/bin/bash

echo "Waiting for Kibana to start..."
sleep 30

# Wait until Kibana is reachable
while true; do
  STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://kibana:5601/app/kibana)

  if [ "$STATUS_CODE" -eq 200 ]; then
    echo "Kibana is ready!"
    break
  else
    echo "Waiting for Kibana... (status: $STATUS_CODE)"
    sleep 5
  fi
done

# Import the dashboard after Kibana is ready
echo "Importing Dashboard"
curl -X POST 'http://kibana:5601/api/saved_objects/_import' -H 'kbn-xsrf: true' --form file=@export.ndjson

# Run model processing
echo "Loading Model's"
python3 process_model.py

# Start the backend server
python3 Node.py
