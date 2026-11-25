#!/usr/bin/env bash
set -euo pipefail

safe="${CERTBOT_DOMAIN//./_}"
rm -f "/run/benxing-acme/$safe.txt" "/run/benxing-acme/$safe.ready"
