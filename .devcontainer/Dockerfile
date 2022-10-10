FROM python:3.9.13

# For jupyter server
EXPOSE 8888

# Install zsh - see https://github.com/deluan/zsh-in-docker
# COPY .devcontainer/.p10k.zsh /root/
# RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
#     -p git \
#     -p https://github.com/zsh-users/zsh-autosuggestions \
#     -p https://github.com/zsh-users/zsh-completions

RUN apt-get update &&\
    apt-get install build-essential -y

RUN apt-get install p7zip-full -y

RUN --mount=type=cache,target=/root/.cache \
    python -m pip install pip==22.2.2

WORKDIR /tmp
COPY requirements.txt requirements.txt
COPY Makefile Makefile
RUN --mount=type=cache,target=/root/.cache \
    make requirements