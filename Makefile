PROJECT = $(shell basename $$(pwd))
ID = pikesley/${PROJECT}
PIHOST = impression.local

default: all

# Laptop targets

build: laptop-only
	docker build \
		--tag ${ID} .

run: laptop-only
	docker run \
		--interactive \
		--tty \
		--name ${PROJECT} \
		--volume $(shell pwd):/opt/${PROJECT} \
		--volume ${HOME}/.ssh:/root/.ssh \
		--rm \
		${ID} bash

# Docker targets

all: docker-only format lint test clean

black: docker-only
	python -m black .

isort: docker-only
	python -m isort .

format: docker-only black isort

lint: docker-only
	python -m pylama

test: docker-only
	python -m pytest \
		--random-order \
		--verbose \
		--capture no \
		--failed-first \
		--exitfirst \
		--cov

font-size-test: docker-only
	python -m pytest tests/font_size_test.py
	@echo
	@echo ">> Generated clockface is at 'tmp/test-font-size.png' <<"
	@echo

clean: docker-only
	@find . -depth -name __pycache__ -exec rm -fr {} \;
	@find . -depth -name .pytest_cache -exec rm -fr {} \;
	@find . -depth -name ".coverage.*" -exec rm {} \;
	@find . -depth -name "*egg-info" -exec rm -fr {} \;

dev-install: docker-only
	 python -m pip install -r requirements-dev.txt

push-code: docker-only clean
	rsync -av /opt/${PROJECT} pi@${PIHOST}:

# Pi targets

setup: pi-only enable-interfaces apt-installs set-python install install-systemd

install: pi-only
	python -m pip install -r requirements.txt

set-python: pi-only
	sudo update-alternatives --install /usr/local/bin/python python /usr/bin/python2 1
	sudo update-alternatives --install /usr/local/bin/python python /usr/bin/python3 2

enable-interfaces: pi-only
	sudo raspi-config nonint do_spi 0
	sudo raspi-config nonint do_i2c 0

apt-installs: pi-only
	sudo apt-get update
	sudo apt-get install -y \
		libjpeg-dev \
		libopenjp2-7-dev \
		libtiff-dev \
		libatlas-base-dev \
		python3-pip

install-systemd: pi-only
	sudo systemctl enable -f /home/pi/impression-clock/systemd/clock.service

# Guardrails

docker-only:
	@if ! [ "$(shell uname -a | grep 'x86_64 GNU/Linux')" ] ;\
	then \
		echo "This target can only be run inside the container" ;\
		exit 1 ;\
	fi

laptop-only:
	@if ! [ "$(shell uname -a | grep 'Darwin')" ] ;\
	then \
		echo "This target can only be run on the laptop" ;\
		exit 1 ;\
	fi

pi-only:
	@if ! [ "$(shell uname -a | grep 'armv.* GNU/Linux')" ] ;\
	then \
		echo "This target can only be run on the Pi" ;\
		exit 1 ;\
	fi
