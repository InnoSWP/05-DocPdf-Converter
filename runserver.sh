#!/bin/bash
case "$OSTYPE" in
  linux*) sh ./linux.sh;;
  msys*) sh ./windows.sh;;
  cygwin*) sh ./windows.sh;;
  *)      echo "unknown: $OSTYPE" ;;
esac