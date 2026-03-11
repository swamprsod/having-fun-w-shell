#!/bin/sh
echo "nameserver 8.8.8.8" | doas tee -a /etc/resolv.conf
