#!/bin/bash
case "$OSTYPE" in
  linux*) sh ./linux-build.sh && sh ./linux-runserver.sh;;
  msys*) sh ./windows-build.sh && sh ./windows-runserver.sh;;
  cygwin*) sh ./windows-build.sh && sh ./windows-runserver.sh;;
  *)      echo "unknown: $OSTYPE" ;;
esac