#!/bin/sh
# rest-install.sh: runs once on Kirpi as root, from the folder holding kimera-rest, its service and font.
# After it, the first console shows the resting screen instead of a login prompt.
# A login prompt stays on the second console: Ctrl+Alt+F2. Back to rest: Ctrl+Alt+F1.
set -eu
[ "$(id -u)" -eq 0 ] || { echo "run with sudo"; exit 1; }
U=${SUDO_USER:?run it with sudo from your own user, not as root directly}
here=$(dirname "$0")

DEBIAN_FRONTEND=noninteractive apt-get install -y -q brightnessctl >/dev/null
usermod -aG video "$U"
udevadm trigger -s backlight -c add || true

install -D -m 644 "$here/kirpi-32x16.psf.gz" /usr/local/share/kimera/kirpi-32x16.psf.gz
install -D -m 755 "$here/kimera-rest" /usr/local/bin/kimera-rest
sed "s/@USER@/$U/" "$here/kimera-rest.service" > /etc/systemd/system/kimera-rest.service
echo "d /run/kimera/jobs 0755 $U $U -" > /etc/tmpfiles.d/kimera.conf
systemd-tmpfiles --create /etc/tmpfiles.d/kimera.conf

systemctl daemon-reload
systemctl disable getty@tty1.service >/dev/null 2>&1 || true
systemctl enable kimera-rest.service >/dev/null 2>&1
systemctl restart kimera-rest.service
sleep 4
systemctl is-active kimera-rest.service
# KIMERA_REST_DUMP=FILE: also write what the first console shows now, as text, to a file of your choosing
if [ -n "${KIMERA_REST_DUMP:-}" ]; then
python3 - > "$KIMERA_REST_DUMP" 2>&1 <<'PY' || true
import subprocess
rows, cols = map(int, subprocess.check_output(['stty', '-F', '/dev/tty1', 'size']).split())
t = open('/dev/vcsu1', 'rb').read().decode('utf-32-le', 'replace')
print(rows, cols)
print('\n'.join(t[r*cols:(r+1)*cols].rstrip() for r in range(rows)))
PY
fi
echo "rest: installed. Look at Kirpi's screen."
