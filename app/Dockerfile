FROM ubuntu:latest

MAINTANER Your Name "chen.8943@osu.edu"

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
