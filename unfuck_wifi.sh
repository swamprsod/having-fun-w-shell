#!/bin/bash
doas ip route del default
doas sv restart dhcpcd
