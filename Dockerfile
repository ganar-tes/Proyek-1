FROM ubuntu:latest

# Install basic tools
RUN apt-get update && apt-get install -y \
    sudo \
    openssh-server \
    wget \
    tmux \
    libsodium23 \
    libsodium-dev \
    curl && \
    apt-get clean

# Enable SSH
RUN mkdir /var/run/sshd
EXPOSE 22
