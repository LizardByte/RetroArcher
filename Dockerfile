FROM python:3.9.6-slim-bullseye

LABEL maintainer="LizardByte"

ENV RETROARCHER_DOCKER=True
ENV TZ=UTC

# setup app directory
WORKDIR /app
COPY . .

# setup python requirements
RUN \
  python -m pip install --no-cache-dir --upgrade pip && \
  python -m pip install --no-cache-dir -r requirements.txt

# compile locales
RUN python scripts/_locale.py --compile

# compile docs
WORKDIR /app/docs
RUN sphinx-build -M html source build

# setup user
RUN \
  groupadd -g 1000 retroarcher && \
  useradd -u 1000 -g 1000 retroarcher

# create config directory
RUN \
  mkdir /config && \
  touch /config/DOCKER
VOLUME /config

CMD ["python", "retroarcher.py"]

EXPOSE 9696
HEALTHCHECK --start-period=90s CMD python retroarcher.py --docker_healthcheck || exit 1
