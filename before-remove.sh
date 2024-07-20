#!/bin/sh
set -ex
deb-systemd-invoke stop unattended-upgrades-prometheus-collector.timer
deb-systemd-invoke disable unattended-upgrades-prometheus-collector.timer
