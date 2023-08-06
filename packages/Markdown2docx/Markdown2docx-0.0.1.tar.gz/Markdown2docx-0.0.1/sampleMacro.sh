#!/bin/bash
cat <<EOF
{'__myarg__':'hello'}
'${say.sh __myarg__}'
EOF
