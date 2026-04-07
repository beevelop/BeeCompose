#!/bin/bash
set -e

if [ "$(ls -A /usr/local/share/ca-certificates/ 2>/dev/null)" ]; then
  update-ca-certificates
fi

source /docker-entrypoint.sh
