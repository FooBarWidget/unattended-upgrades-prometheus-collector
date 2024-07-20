# Prometheus node collector for unattended-upgrades

Allows monitoring [unattended-upgrades](https://github.com/mvo5/unattended-upgrades) runs.

- Monitors the last time it ran successfully.
- Only for unattended-upgrades >= 2.11: monitors the last time it failed.

## How it works

On unattended-upgrades < 2.11, a systemd timer runs every hour and checks the timestamp of the file `/var/lib/apt/periodic/upgrade-stamp`. This timestamp is updated by unattended-upgrades every time it runs successfully. Unfortunately, unattended-upgrades < 2.11 provides no way to check when it last failed.

On unattended-upgrades >= 2.11, we install an unattended-upgrades plugin. When unattended-upgrades completes, our plugin takes note of whether unattended-upgrades succeeded or failed.

We publish metrics to one of these files depending on whether the run succeeded or failed (again, failure detection is only supported for unattended-upgrades >= 2.11):

- /var/lib/prometheus/node-exporter/unattended-upgrades-last-successful-run-timestamp.prom
- /var/lib/prometheus/node-exporter/unattended-upgrades-last-failed-run-timestamp.prom

This program is meant to be used in combination with the Prometheus node exporter's textfile collector, which reads from the above files every time it's scraped.

## Installation

Download the .deb file from the [Releases section](https://github.com/FooBarWidget/unattended-upgrades-prometheus-collector/releases) and install it. The package is distribution- and platform-independent.

Ansible example (be sure to update the URL according to latest release):

```yaml
- name: Install unattended-upgrades-prometheus-collector
  apt:
    deb: https://github.com/FooBarWidget/unattended-upgrades-prometheus-collector/releases/download/v1.0.0/unattended-upgrades-prometheus-collector_1.0.0_all.deb
```

## Metrics

- `unattended_upgrades_last_successful_run_timestamp` — Timestamp of the last unattended-upgrades successful run.
- `unattended_upgrades_last_failed_run_timestamp` — Timestamp of the last unattended-upgrades failed run (unattended-upgrades >= 2.11 only).

## Alerting rule

```yaml
- alert: UnattendedUpgradesFailed
  expr: (unattended_upgrades_last_failed_run_timestamp > unattended_upgrades_last_successful_run_timestamp) > (unattended_upgrades_last_successful_run_timestamp < (time() - 2 * 24 * 60 * 60))
  for: 10m
  labels:
    severity: warning
  annotations:
    summary: Unattended-upgrades failed or haven't run for two days
    description: Please check /var/log/unattended-upgrades/unattended-upgrades.log.
```
