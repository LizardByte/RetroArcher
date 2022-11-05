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

# setup app directory
WORKDIR /build
COPY . .

# setup python requirements
RUN python -m pip install --no-cache-dir --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements.txt

# compile locales
RUN python scripts/_locale.py --compile

# setup npm and dependencies
WORKDIR /build/web
RUN npm install

# compile docs
WORKDIR /build/docs
RUN sphinx-build -M html source build

FROM retroarcher-base as retroarcher

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
