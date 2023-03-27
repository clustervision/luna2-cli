#!/bin/sh
if [ -n "$VISUAL" ]; then
  exec $VISUAL "$@"
elif [ -n "$EDITOR" ]; then
  exec $EDITOR "$@"
elif type sensible-editor >/dev/null 2>/dev/null; then
  exec sensible-editor "$@"
#elif cmd=$(xdg-mime query default ) 2>/dev/null; [ -n "$cmd" ]; then
#  exec "$cmd" "$@"
else
  editors='nano joe vi'
  if [ -n "$DISPLAY" ]; then
    editors="gedit kate $editors"
  fi
  for x in $editors; do
    if type "$x" >/dev/null 2>/dev/null; then
      exec "$x" "$@"
    fi
  done
fi
