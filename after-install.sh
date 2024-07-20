#!/bin/sh
set -ex
if ! grep -q PluginManager /usr/bin/unattended-upgrades; then
    systemctl --system daemon-reload
    deb-systemd-invoke enable unattended-upgrades-prometheus-collector.timer
    deb-systemd-invoke start unattended-upgrades-prometheus-collector.timer
fi
