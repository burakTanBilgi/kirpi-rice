#!/bin/sh
# login-install.sh: runs once on Kirpi as root:  sudo sh login-install.sh
#   1. password login on tty1 at boot; the rest screen starts inside that session (no autologin)
#   2. the deck's terminal is a plain login shell (no su, no password)
# Safe to run again. Undo (back to autologin): sudo sh login-install.sh --undo
set -eu
[ "$(id -u)" -eq 0 ] || { echo "run with sudo"; exit 1; }
U=${SUDO_USER:?run it with sudo from your own user, not as root directly}
here=$(cd "$(dirname "$0")" && pwd)
HOOK=/etc/profile.d/kimera-rest.sh
say() { echo "  $*"; }

if [ "${1:-}" = "--undo" ]; then
  echo "undo: back to autologin"
  [ -f /etc/systemd/system/kimera-rest.service ] || { echo "no kimera-rest.service; run rest-install.sh; nothing was changed"; exit 1; }
  rm -f "$HOOK" && say "removed $HOOK"
  systemctl disable getty@tty1.service >/dev/null 2>&1 || true
  systemctl daemon-reload
  systemctl enable kimera-rest.service >/dev/null 2>&1 && say "kimera-rest.service enabled, getty@tty1 disabled"
  systemctl restart kimera-rest.service && say "rest screen started by systemd (autologin)"
  say "kept: the deck's login-shell terminal"
  exit 0
fi

echo "login-install:"
# the rest screen and its helpers must exist; this script does not install them
[ -x /usr/local/bin/kimera-rest ] || { echo "kimera-rest not installed; run rest-install.sh first"; exit 1; }

# 1. the hook
sed "s/@USER@/$U/" "$here/kimera-rest-login.sh" > "$HOOK.new"
if cmp -s "$HOOK.new" "$HOOK" 2>/dev/null; then rm "$HOOK.new"; say "hook already in place"
else mv "$HOOK.new" "$HOOK"; chmod 644 "$HOOK"; say "wrote $HOOK (tty1 only, user $U, never ssh)"; fi

# as the user: setfont works on the user's own tty; brightnessctl needs group video (and its udev rule)
if id -nG "$U" | tr ' ' '\n' | grep -qx video; then say "$U is in group video (backlight ok)"
else usermod -aG video "$U"; say "added $U to group video (takes effect at the next login)"; fi
command -v brightnessctl >/dev/null || { DEBIAN_FRONTEND=noninteractive apt-get install -y -q brightnessctl >/dev/null; say "installed brightnessctl"; }
install -m 755 "$here/kimera-rest" /usr/local/bin/kimera-rest

# 2. the deck's terminal (new panel file); sway runs from the login session via logind
if [ -f "$here/deck/kimera-deck-panel" ]; then
  install -m 755 "$here/deck/kimera-deck-panel" /usr/local/bin/kimera-deck-panel
  say "installed the deck panel (terminal = foot --login-shell, no su)"
fi

# 3. the switch: getty on tty1 back on, systemd autologin service off (file kept for rollback)
systemctl disable kimera-rest.service >/dev/null 2>&1 || true
systemctl enable getty@tty1.service >/dev/null 2>&1
systemctl daemon-reload
say "kimera-rest.service disabled, getty@tty1 enabled (the running rest screen ends now; tty1 shows a login)"
systemctl stop kimera-rest.service || true
systemctl restart getty@tty1.service
echo "done. Log in on Kirpi's screen: the rest screen starts after the password. ssh is unaffected."
