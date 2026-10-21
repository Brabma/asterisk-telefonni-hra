#!/usr/bin/env bash
set -Eeuo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Run through verified sudo: sudo bash scripts/configure-odorik-firewall.sh" >&2
  exit 1
fi

# SIP port must match the transport bind in pjsip (see asterisk/pjsip-odorik.conf.example).
sip_port="${SIP_PORT:-5060}"

sip_addresses=(
  81.31.45.51
  89.185.255.52
)

media_networks=(
  89.185.255.32/27
  81.31.45.32/27
  81.31.43.232/29
  81.31.43.192/28
)

for address in "${sip_addresses[@]}"; do
  ufw allow proto udp from "$address" to any port "$sip_port" comment 'Odorik SIP'
done

for network in "${media_networks[@]}"; do
  ufw allow proto udp from "$network" to any port 10000:20000 comment 'Odorik RTP'
done

ufw status verbose
