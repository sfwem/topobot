#!/bin/bash

set -ex

echo "Inside docker-entrypoint.sh"

if [ "$1" = "topobot" ]; then
  echo "Starting topbot"
  topobot ${TOPOBOT_MODE}
  exit
fi

echo "Executing '$@'"

exec "$@"
