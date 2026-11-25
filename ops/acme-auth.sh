#!/usr/bin/env bash
set -euo pipefail

domain="${CERTBOT_DOMAIN:?}"
case "$domain" in
    essencetherapy.cn|www.essencetherapy.cn) ;;
    *) exit 2 ;;
esac

safe="${domain//./_}"
dir=/run/benxing-acme
install -d -m 700 "$dir"
rm -f "$dir/$safe.ready"
printf '%s\n' "${CERTBOT_VALIDATION:?}" > "$dir/$safe.txt"
chmod 600 "$dir/$safe.txt"

for ((i=0; i<900; i++)); do
    if test -f "$dir/$safe.ready"; then
        rm -f "$dir/$safe.ready"
        exit 0
    fi
    sleep 2
done

echo 'DNS confirmation timed out' >&2
exit 1
