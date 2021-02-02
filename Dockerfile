FROM python:3.7

RUN apt-get update && apt-get install -y make rsync
RUN python -m pip install --upgrade pip

ENV PROJECT impression-clock
ENV PLATFORM docker

WORKDIR /opt/${PROJECT}

COPY ./ /opt/${PROJECT}

RUN make dev-install

COPY docker-config/bashrc /root/.bashrc
