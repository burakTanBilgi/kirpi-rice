#!/bin/sh
# Run with sudo: the machine never goes to sleep, lid closed or not. For a machine that stays plugged in on a desk:
# a laptop that cannot sleep gets hot in a bag. Undo: delete /etc/systemd/logind.conf.d/10-kimera-awake.conf,
# then  systemctl unmask sleep.target suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target
set -e
[ "$(id -u)" -eq 0 ] || { echo "run with sudo"; exit 1; }
mkdir -p /etc/systemd/logind.conf.d
cat > /etc/systemd/logind.conf.d/10-kimera-awake.conf <<'C'
[Login]
HandleLidSwitch=ignore
HandleLidSwitchExternalPower=ignore
HandleLidSwitchDocked=ignore
HandleSuspendKey=ignore
HandleHibernateKey=ignore
IdleAction=ignore
C
systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target suspend-then-hibernate.target
systemctl kill -s HUP systemd-logind
echo "kirpi: it will not sleep any more, lid closed or open"
