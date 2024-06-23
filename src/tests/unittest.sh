#!/bin/bash
if [[ "$1" ]];then
  IP="$1"
else
  IP=$(hostname -i)
fi
echo "$IP"
curl http://"$IP":80 # -o /dev/null -s
RESULT=$?
if [[ RESULT -eq 0 ]]; then
    echo "Command succeeded"
    echo "Exit Code" $RESULT
else
    echo "Command failed"
    echo "Exit Code" $RESULT
    exit 1
fi
exit 0