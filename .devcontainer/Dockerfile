FROM python:3.9.13

# For jupyter server
EXPOSE 8888

RUN apt-get update &&\
    apt-get install build-essential -y

RUN apt-get install p7zip-full -y

RUN --mount=type=cache,target=/root/.cache \
    python -m pip install pip==22.2.2

WORKDIR /tmp
COPY requirements.txt requirements.txt
RUN --mount=type=cache,target=/root/.cache \
    python -m pip install -r requirements.txt
