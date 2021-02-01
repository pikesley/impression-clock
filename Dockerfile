FROM python:3.7

RUN apt-get update && apt-get install -y make rsync

ENV PROJECT impression-clock


WORKDIR /opt/${PROJECT}

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN ln -s /root/.poetry/bin/poetry /usr/local/bin/

COPY ./ /opt/${PROJECT}

RUN poetry config virtualenvs.create false
RUN make --makefile make/Makefile.docker install

COPY docker-config/bashrc /root/.bashrc
