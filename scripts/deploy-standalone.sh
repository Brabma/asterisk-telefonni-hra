#!/usr/bin/env bash
set -Eeuo pipefail

if [[ ${EUID} -ne 0 ]]; then
  echo "Run as root: sudo bash scripts/deploy-standalone.sh" >&2
  exit 1
fi

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo_dir="${1:-$(cd -- "$script_dir/.." && pwd)}"
story_file="$repo_dir/game/story.json"
source_audio="$repo_dir/audio"
build_dir="$repo_dir/build"
source_dialplan="$build_dir/extensions_telefonni_adventura.conf"
asterisk_dir="/etc/asterisk"
main_dialplan="$asterisk_dir/extensions.conf"
game_dialplan="$asterisk_dir/extensions_telefonni_adventura.conf"
sound_dir="/usr/share/asterisk/sounds/en/custom/telefonni-adventura"
state_dir="/var/lib/telefonni-adventura"
expected_audio_file="$state_dir/expected-audio-count"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
backup_dir="/var/backups/telefonni-adventura/$timestamp"

[[ -f "$story_file" ]] || { echo "Missing $story_file" >&2; exit 1; }
[[ -d "$source_audio" ]] || { echo "Missing $source_audio" >&2; exit 1; }
[[ -f "$main_dialplan" ]] || { echo "Missing $main_dialplan" >&2; exit 1; }
systemctl is-active --quiet asterisk || { echo "Asterisk is not active." >&2; exit 1; }

echo "[1/7] Validating the story and generating the dialplan"
install -d -m 0755 "$build_dir"
python3 "$repo_dir/tools/build_dialplan.py" "$story_file" "$source_dialplan"

expected_audio_count="$(python3 -c 'import json,sys; data=json.load(open(sys.argv[1],encoding="utf-8")); print(len(data["nodes"])+1)' "$story_file")"
source_audio_count="$(find "$source_audio" -type f -name '*.wav' | wc -l)"
[[ "$source_audio_count" -eq "$expected_audio_count" ]] || {
  echo "Expected $expected_audio_count WAV files, found $source_audio_count." >&2
  exit 1
}

echo "[2/7] Backing up the current state"
install -d -m 0700 "$backup_dir"
cp -a "$main_dialplan" "$backup_dir/extensions.conf"
[[ ! -f "$game_dialplan" ]] || cp -a "$game_dialplan" "$backup_dir/extensions_telefonni_adventura.conf"
if [[ -d "$sound_dir" ]]; then
  cp -a "$sound_dir" "$backup_dir/sounds"
fi
if [[ -f "$expected_audio_file" ]]; then
  cp -a "$expected_audio_file" "$backup_dir/expected-audio-count"
fi

restore_backup() {
  echo "Deployment failed; restoring the previous state." >&2
  cp -a "$backup_dir/extensions.conf" "$main_dialplan"
  if [[ -f "$backup_dir/extensions_telefonni_adventura.conf" ]]; then
    cp -a "$backup_dir/extensions_telefonni_adventura.conf" "$game_dialplan"
  else
    rm -f "$game_dialplan"
  fi
  rm -rf "$sound_dir"
  if [[ -d "$backup_dir/sounds" ]]; then
    cp -a "$backup_dir/sounds" "$sound_dir"
  fi
  if [[ -f "$backup_dir/expected-audio-count" ]]; then
    install -d -o root -g root -m 0755 "$state_dir"
    cp -a "$backup_dir/expected-audio-count" "$expected_audio_file"
  else
    rm -f "$expected_audio_file"
  fi
  asterisk -rx 'dialplan reload' >/dev/null 2>&1 || true
}
trap restore_backup ERR

echo "[3/7] Installing the generated game dialplan"
install -o root -g asterisk -m 0640 "$source_dialplan" "$game_dialplan"

echo "[4/7] Creating an isolated public inbound context"
if ! grep -Fq '; BEGIN TELEFONNI ADVENTURA STANDALONE' "$main_dialplan"; then
  cat >> "$main_dialplan" <<'EOF'

; BEGIN TELEFONNI ADVENTURA STANDALONE
#include extensions_telefonni_adventura.conf
[telefonni-adventura-public]
exten => s,1,Goto(telefonni-adventura-entry,555,1)
exten => _X!,1,Goto(telefonni-adventura-entry,555,1)
; END TELEFONNI ADVENTURA STANDALONE
EOF
fi

echo "[5/7] Installing telephone audio"
rm -rf "$sound_dir"
install -d -o asterisk -g asterisk -m 0755 "$sound_dir"
cp -a "$source_audio"/. "$sound_dir"/
chown -R asterisk:asterisk "$sound_dir"
install -d -o root -g root -m 0755 "$state_dir"
printf '%s\n' "$expected_audio_count" > "$expected_audio_file"
chown root:root "$expected_audio_file"
chmod 0644 "$expected_audio_file"

echo "[6/7] Reloading and verifying Asterisk"
asterisk -rx 'dialplan reload'
entry_output="$(asterisk -rx 'dialplan show 555@telefonni-adventura-public' 2>&1)"
printf '%s\n' "$entry_output"
grep -Fq 'telefonni-adventura-entry' <<< "$entry_output"
first_scene_output="$(asterisk -rx 'dialplan show s@telefonni-adventura-last-call' 2>&1)"
printf '%s\n' "$first_scene_output"
grep -Fq 'telefonni-adventura-last-call' <<< "$first_scene_output"

echo "[7/7] Installing a systemd health check"
install -o root -g root -m 0755 \
  "$repo_dir/scripts/health-check.sh" \
  /usr/local/sbin/telefonni-adventura-health-check
install -o root -g root -m 0644 \
  "$repo_dir/scripts/systemd/telefonni-adventura-health.service" \
  /etc/systemd/system/telefonni-adventura-health.service
install -o root -g root -m 0644 \
  "$repo_dir/scripts/systemd/telefonni-adventura-health.timer" \
  /etc/systemd/system/telefonni-adventura-health.timer
systemctl daemon-reload
systemctl enable --now telefonni-adventura-health.timer
/usr/local/sbin/telefonni-adventura-health-check

cat > "$backup_dir/DEPLOYMENT.txt" <<EOF
Telephone adventure deployed: $timestamp
Public dialplan context: telefonni-adventura-public
Internal game extension: 555
Installed WAV files: $source_audio_count
Rollback source: $backup_dir
EOF

trap - ERR
echo
echo "Standalone game deployment succeeded."
echo "Point the trusted SIP provider endpoint to context: telefonni-adventura-public"
echo "Backup: $backup_dir"
