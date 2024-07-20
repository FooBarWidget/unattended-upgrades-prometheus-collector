#!/usr/bin/env bash
set -ex
exec fpm \
    --verbose \
    --force \
    -s dir \
    -t deb \
    -n unattended-upgrades-prometheus-collector \
    -v 1.0.0 \
    --license MIT \
    --architecture all \
    --depends python3-minimal \
    --description 'Prometheus node collector for unattended-upgrades' \
    --maintainer 'Hongli Lai <hongli@hongli.nl>' \
    --after-install after-install.sh \
    --after-remove after-remove.sh \
    --before-remove before-remove.sh \
    unattended-upgrades-prometheus-collector.service=/lib/systemd/system/ \
    unattended-upgrades-prometheus-collector.timer=/lib/systemd/system/ \
    timer.py=/usr/share/unattended-upgrades-prometheus-collector/ \
    reporting.py=/usr/share/unattended-upgrades-prometheus-collector/ \
    plugin.py=/usr/share/unattended-upgrades/plugins/unattended-upgrades-prometheus-collector.py
