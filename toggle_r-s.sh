#!/bin/env sh

if pgrep -x "wf-recorder" > /dev/null; then
	pkill wf-recorder
else
	wf-recorder --audio -f "/home/rsod/screenshots/a-$(date +'%Y-%m-%d_%H-%M-%S').mp4" --codec h264_vaapi -d /dev/dri/renderD128 -a "alsa_input.pci-0000_00_1b.0.analog-stereo"
fi
