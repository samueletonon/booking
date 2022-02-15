# syntax=docker/dockerfile:1
FROM python:3.10-slim-bullseye


ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app
COPY . /app
WORKDIR /app

#RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt && useradd -U app_user && install -d -m 0755 -o app_user -g app_user /app/static
RUN chown -R app_user:app_user /app
RUN chmod ugo+x docker/*.sh 
USER app_user:app_user

#ENTRYPOINT [ "docker/entrypoint.sh" ]
#CMD [ "docker/start.sh" ]
