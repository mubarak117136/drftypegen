FROM registry.gitlab.com/codesigntheory/django-base:latest
ARG PIPENVDEV=--dev
ADD Pipfile* /app/server/
WORKDIR /app/server/
ENTRYPOINT [ "pipenv", "run"]
RUN pipenv sync ${PIPENVDEV} && \
    apt-get clean && apt-get auto-clean
ADD . /app/server/
