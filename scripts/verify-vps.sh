#!/usr/bin/env bash
set -Eeuo pipefail

echo "== Operating system =="
# Values come from the target system, not a file shipped with this repository.
# shellcheck source=/dev/null
. /etc/os-release
printf '%s\n' "$PRETTY_NAME"

echo "== Resources =="
printf 'CPU cores: '
nproc
free -h
df -h /

echo "== Asterisk =="
asterisk -V
systemctl --no-pager --full status asterisk | sed -n '1,8p'

echo "== Game dialplan =="
asterisk -rx 'dialplan show 555@telefonni-adventura-public'

echo "== Game audio =="
actual_audio_count="$(find /usr/share/asterisk/sounds/en/custom/telefonni-adventura -type f -name '*.wav' | wc -l)"
expected_audio_count="$(</var/lib/telefonni-adventura/expected-audio-count)"
printf 'Audio files: %s/%s\n' "$actual_audio_count" "$expected_audio_count"

echo "== Current health check =="
/usr/local/sbin/telefonni-adventura-health-check

echo "== Listening UDP sockets =="
ss -lunp

echo "== Health timer =="
systemctl --no-pager list-timers telefonni-adventura-health.timer

echo "== Recent health results =="
journalctl -u telefonni-adventura-health.service -n 10 --no-pager
