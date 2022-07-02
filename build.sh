#!/bin/bash
case "$OSTYPE" in
  linux*) sh linux-build.sh;;
  msys*) sh windows-build.sh;;
  cygwin*) sh windows-build.sh;;
  *)      echo "unknown: $OSTYPE" ;;
esac