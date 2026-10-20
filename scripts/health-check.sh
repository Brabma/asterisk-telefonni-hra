#!/usr/bin/env bash
set -Eeuo pipefail

sound_dir="/usr/share/asterisk/sounds/en/custom/telefonni-adventura"
expected_audio_file="/var/lib/telefonni-adventura/expected-audio-count"

systemctl is-active --quiet asterisk
dialplan_output="$(asterisk -rx 'dialplan show 555@telefonni-adventura-public' 2>&1)"
grep -Fq 'telefonni-adventura-entry' <<< "$dialplan_output"
[[ -r "$expected_audio_file" ]] || {
  echo "Missing expected audio count: $expected_audio_file" >&2
  exit 1
}
expected_audio_count="$(<"$expected_audio_file")"
[[ "$expected_audio_count" =~ ^[1-9][0-9]*$ ]] || {
  echo "Invalid expected audio count: $expected_audio_count" >&2
  exit 1
}
audio_count="$(find "$sound_dir" -type f -name '*.wav' | wc -l)"
if [[ "$audio_count" -ne "$expected_audio_count" ]]; then
  echo "Audio count mismatch: expected $expected_audio_count, found $audio_count in $sound_dir" >&2
  exit 1
fi

echo "OK asterisk=active dialplan=loaded audio_files=$audio_count/$expected_audio_count"
