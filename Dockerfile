# artifacts: false
# platforms: linux/amd64,linux/arm64/v8
FROM python:3.12-slim-bookworm AS base

FROM base AS build

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# install build dependencies
RUN <<_DEPS
#!/bin/bash
set -e

dependencies=(
  "build-essential"
  "libjpeg-dev"  # pillow
  "npm"  # web dependencies
  "pkg-config"
  "libopenblas-dev"
  "zlib1g-dev"  # pillow
)
apt-get update -y
apt-get install -y --no-install-recommends "${dependencies[@]}"
apt-get clean
rm -rf /var/lib/apt/lists/*
_DEPS

# python virtualenv
RUN python -m venv /opt/venv
# use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# setup app directory
WORKDIR /build
COPY . .

# setup python requirements
RUN <<_REQUIREMENTS
#!/bin/bash
set -e
python -m pip install --no-cache-dir --upgrade pip setuptools wheel
python -m pip install --no-cache-dir -r requirements.txt
_REQUIREMENTS

# compile locales
RUN python scripts/_locale.py --compile

# setup npm and dependencies
RUN <<_NPM
#!/bin/bash
set -e
npm install
mv -f ./node_modules/ ./web/
_NPM

# compile docs
WORKDIR /build/docs
RUN sphinx-build -M html source build

FROM base AS app

# copy app from builder
COPY --from=build /build/ /app/

# copy python venv
COPY --from=build /opt/venv/ /opt/venv/
# use the venv
ENV PATH="/opt/venv/bin:$PATH"
# site-packages are in /opt/venv/lib/python<version>/site-packages/

# setup remaining env variables
ENV RETROARCHER_DOCKER=True

# network setup
EXPOSE 9696

# setup user
ARG PGID=1000
ENV PGID=${PGID}
ARG PUID=1000
ENV PUID=${PUID}
ENV TZ="UTC"
ARG UNAME=lizard
ENV UNAME=${UNAME}

ENV HOME=/home/$UNAME

# setup user
RUN <<_SETUP_USER
#!/bin/bash
set -e
groupadd -f -g "${PGID}" "${UNAME}"
useradd -lm -d ${HOME} -s /bin/bash -g "${PGID}" -u "${PUID}" "${UNAME}"
mkdir -p ${HOME}/.config/retroarcher
ln -s ${HOME}/.config/retroarcher /config
chown -R ${UNAME} ${HOME}
_SETUP_USER

# mounts
VOLUME /config

USER ${UNAME}
WORKDIR ${HOME}

ENTRYPOINT ["python", "./src/retroarcher.py"]
HEALTHCHECK --start-period=90s CMD python ./src/retroarcher.py --docker_healthcheck || exit 1
