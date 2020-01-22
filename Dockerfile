# Dockerfile for TopoBot.
# Run TopoBot in a Docker Container
#
# Author:: Greg Albrecht W2GMD <oss@undef.net>
# Copyright:: Copyright 2020 Greg Albrecht
# License:: Apache License, Version 2.0
# Source:: https://github.com/ampledata/topobot
#

FROM python:3.7-slim-buster

# Source for OLSR Topopology:
ENV TOPO_HOST=localnode.local.mesh

# What mode to run bot in, -p, -d or -b?
ENV TOPOBOT_MODE=-b

# Slack API Token
ENV SLACKBOT_API_TOKEN=changeme

ADD . .
RUN python setup.py install

# Allows us to override the startup cmd at runtime:
ENTRYPOINT ["./docker-scripts/docker-entrypoint.sh"]

CMD ["topobot"]

# Metadata about this container:
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="TopBot" \
      org.label-schema.description="AREDN Mesh Network Topology Bot" \
      org.label-schema.url="https://github.com/ampledata/topobot" \
      org.label-schema.vcs-url="https://github.com/ampledata/topobot" \
      org.label-schema.vcs-ref="https://github.com/ampledata/topobot" \
      org.label-schema.vendor="Greg Albrecht" \
      org.label-schema.version="$VERSION" \
      org.label-schema.schema-version="1.0" \
      org.label-schema.author="Greg Albrecht" \
      org.label-schema.docker.dockerfile="/Dockerfile" \
      org.label-schema.license="Apache License, Version 2.0" \
      org.label-schema.docker.cmd="docker run -d \
        -e 'TOPO_HOST=changeme'\
        ampledata/topobot" \
      maintainer="oss@undef.net"
