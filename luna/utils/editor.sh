#!/bin/sh

# This code is part of the TrinityX software suite
# Copyright (C) 2025  ClusterVision Solutions b.v.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>


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
