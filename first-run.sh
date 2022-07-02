#!/bin/bash
case "$OSTYPE" in
  linux*)
    chmod +x linux-build.sh
    sh linux-build.sh
    chmod +x linux-runserver.sh
    sh linux-runserver.sh;;
  msys*)
    chmod +x windows-build.sh
    source windows-build.sh
    chmod +x windows-runserver.sh
    source windows-runserver.sh;;
  cygwin*)
    chmod +x windows-build.sh
    source windows-build.sh
    chmod +x windows-runserver.sh
    source windows-runserver.sh;;
  *)      echo "unknown: $OSTYPE" ;;
esac