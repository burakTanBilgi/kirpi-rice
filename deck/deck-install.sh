#!/bin/sh
# deck-install.sh: runs once on Kirpi as root, from the folder holding the deck's files.
# After it, any key on the resting screen opens the deck.
set -eu
[ "$(id -u)" -eq 0 ] || { echo "run with sudo"; exit 1; }
U=${SUDO_USER:?run it with sudo from your own user, not as root directly}
here=$(dirname "$0")

echo "installing sway, foot and the drawing libraries (a few minutes) ..."
log=$(mktemp)
DEBIAN_FRONTEND=noninteractive apt-get install -y -q --no-install-recommends \
  sway swayidle foot foot-terminfo python3-gi python3-gi-cairo gir1.2-gtk-3.0 \
  libgl1-mesa-dri fontconfig grim btop > "$log" 2>&1 \
  || { tail -5 "$log"; rm -f "$log"; echo "the packages did not install; nothing else was changed"; exit 1; }
rm -f "$log"

install -d /usr/local/share/fonts/kimera /usr/local/share/kimera /etc/kimera
install -m 644 "$here"/fonts/*.ttf "$here"/fonts/OFL-*.txt /usr/local/share/fonts/kimera/
fc-cache -f /usr/local/share/fonts/kimera
install -m 644 "$here/kirpi-deck.png" /usr/local/share/kimera/kirpi-deck.png
install -m 755 "$here/kimera-deck-panel" /usr/local/bin/kimera-deck-panel
install -m 644 "$here/foot.ini" /etc/kimera/foot.ini
layout=$(. /etc/default/keyboard 2>/dev/null; echo "${XKBLAYOUT:-us}")
sed "s/@LAYOUT@/$layout/" "$here/deck.sway" > /etc/kimera/deck.sway

# one frame drawn to a file as the user: proves the fonts and libraries are all there
shot=$(su "$U" -c 'mktemp --suffix=.png')
su "$U" -c "/usr/local/bin/kimera-deck-panel --png '$shot'"
[ -s "$shot" ] || { rm -f "$shot"; echo "the deck could not draw; nothing was switched on"; exit 1; }
rm -f "$shot"

# last, so the resting screen only offers the deck once everything is in place
install -m 755 "$here/kimera-deck" /usr/local/bin/kimera-deck
echo "deck: installed (keyboard: $layout). Press any key on Kirpi's resting screen."
