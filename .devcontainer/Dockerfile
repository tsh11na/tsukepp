FROM python:3.10
ENV PYTHONBUFFERED 1

ARG USERNAME=vscode
ARG USER_UID=1234
ARG USER_GID=${USER_UID}

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

RUN apt-get update && apt-get upgrade -y \
    && pip3 install --upgrade pip

COPY requirements.txt .
USER ${USERNAME}
