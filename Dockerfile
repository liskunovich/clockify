FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get update && apt-get install -y python3-pip
ENV BOT_TOKEN=token
ENV API_KEY=key
COPY . /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
ENTRYPOINT ["python3", "main.py"]