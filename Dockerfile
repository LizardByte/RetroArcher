FROM python:3.9.12-slim-bullseye

LABEL maintainer="RetroArcher"

ENV RETROARCHER_DOCKER=True

COPY requirements.txt .
COPY docs .
COPY locale .
COPY pyra .
COPY scripts .
COPY web .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "retroarcher.py"]

EXPOSE 9696
HEALTHCHECK --start-period=90s CMD curl -ILfSs http://localhost:9696/status > /dev/null || curl -ILfkSs https://localhost:9696/status > /dev/null || exit 1
