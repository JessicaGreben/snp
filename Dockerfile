FROM ubuntu:16.04

RUN apt-get update && apt-get -y install \
    awscli \
    git \
    vim  \
    netcat \
    python-dev \
    python-pip \
    build-essential

COPY . /tmp/

RUN pip install -r /tmp/requirements.txt

EXPOSE 8080

WORKDIR /tmp/

CMD ["python", "server.py"]
