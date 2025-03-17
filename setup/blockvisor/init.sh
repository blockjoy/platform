#!/bin/bash

dev=$(ip --json r | jq -r '.[0].dev')
gateway=$(ip --json r | jq -r '.[0].gateway')
ipaddr=$(ip --json r | jq -r '.[1].prefsrc')

# Wait until /data/success exists
if [ -f "/data/success" ]; then
  printf "/data/success already exists. Skipping wait.\n"
else
  while [ ! -f "/data/success" ]; do
    sleep 2
  done
  printf "Success file detected?  Continuing blockvisor setup...\n"
fi

printf "Database has been initialized\n"

# Run bvup if blockvisor.json does not exist
if [ ! -f "/etc/blockvisor.json" ]; then
  bvup --region dev --api http://envoy:8090 --use-host-network --gateway-ip "$gateway" --host-ip "$ipaddr" --ifa "$dev" --skip-download Hqzv8Ux7LWRR -y
else
  printf "Host already configured, skipping bvup\n"
fi

printf "\nStarting Blockvisord...\n"
/opt/blockvisor/blockvisor/bin/blockvisord
