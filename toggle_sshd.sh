#!/bin/bash

if pgrep -x "sshd" > /dev/null; then
	doas pkill sshd
else
    	doas /usr/bin/sshd -f /etc/ssh/sshd_config
	echo "start"
fi
