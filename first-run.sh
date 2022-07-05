#!/bin/bash
case "$OSTYPE" in
  linux*)
    source linux-build.sh
    source linux-runserver.sh;;
  msys*)
    source windows-build.sh
    source windows-runserver.sh;;
  cygwin*)
    source windows-build.sh
    source windows-runserver.sh;;
  *)
    echo "unknown: $OSTYPE" ;;
esac
