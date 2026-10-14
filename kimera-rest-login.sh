# /etc/profile.d/kimera-rest.sh: the resting screen starts in the tty1 login session, after the password.
# Only the real first console, only the user who installed it, never ssh, never a second console.
if [ "$(id -un)" = "@USER@" ] && [ -z "${SSH_CONNECTION:-}${SSH_TTY:-}" ] \
   && [ -t 0 ] && [ "$(tty 2>/dev/null)" = /dev/tty1 ] \
   && [ -z "${KIMERA_REST_RUNNING:-}" ] && [ -x /usr/local/bin/kimera-rest ]; then
  export KIMERA_REST_RUNNING=1 TERM=linux
  exec /usr/local/bin/kimera-rest
fi
