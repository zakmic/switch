FROM python:3.8
WORKDIR /app
COPY . .
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y libgl1
RUN chmod +x /app/entrypoint.sh
EXPOSE 3001 8089 5001
CMD ["./entrypoint.sh"]
