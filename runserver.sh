#!/bin/bash
case "$OSTYPE" in
  linux*) sh linux-runserver.sh;;
  msys*) sh windows-runserver.sh;;
  cygwin*) sh windows-runserver.sh;;
  *)      echo "unknown: $OSTYPE" ;;
esac