# artifacts: false
# platforms: linux/386,linux/amd64
FROM python:3.9.6-slim-bullseye as retroarcher-base

FROM retroarcher-base as retroarcher-build

# install build dependencies
RUN apt-get update -y \
     && apt-get install -y --no-install-recommends \
        build-essential \
        nodejs \
        npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# python virtualenv
RUN python -m venv /opt/venv
# use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# setup app directory
WORKDIR /build
COPY . .

# setup python requirements
# do not use `python -m pip ...` or packages do not get put into venv, since it's not activated like normal
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# compile locales
RUN python scripts/_locale.py --compile

# setup npm and dependencies
WORKDIR /build/web
RUN npm install

# compile docs
WORKDIR /build/docs
RUN sphinx-build -M html source build

FROM retroarcher-base as retroarcher

# copy python venv
COPY --from=retroarcher-build /opt/venv/ /opt/venv/
# use the venv
ENV PATH="/opt/venv/bin:$PATH"
# site-packages are in /opt/venv/lib/python<version>/site-packages/

# copy app from builder
COPY --from=retroarcher-build /build/ /app/

# setup user
RUN groupadd -g 1000 retroarcher && \
    useradd -u 1000 -g 1000 retroarcher

# create config directory
RUN mkdir /config && \
    touch /config/DOCKER
VOLUME /config

CMD ["python", "retroarcher.py"]

EXPOSE 9696
HEALTHCHECK --start-period=90s CMD python retroarcher.py --docker_healthcheck || exit 1
