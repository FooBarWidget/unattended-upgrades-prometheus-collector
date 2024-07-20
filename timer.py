#!/usr/bin/env python3
import os
import sys
import reporting


UPGRADE_TIMESTAMP_PATH = os.getenv(
    'UPGRADE_TIMESTAMP_PATH', '/var/lib/apt/periodic/upgrade-stamp')


def unattended_upgrades_supports_plugins():
    try:
        with open('/usr/bin/unattended-upgrades', 'r', encoding='UTF-8') as f:
            return f.read().find('PluginManager') != -1
    except FileNotFoundError:
        print("Warning: unattended-upgrades not installed.", file=sys.stderr)
        return None


def last_successful_run_timestamp():
    try:
        return int(os.path.getmtime(UPGRADE_TIMESTAMP_PATH))
    except FileNotFoundError:
        print("Warning: unattended-upgrades timestamp file ({}) not found. Not reporting any metrics.".format(
            UPGRADE_TIMESTAMP_PATH), file=sys.stderr)


def main():
    if unattended_upgrades_supports_plugins():
        print("Warning: unattended-upgrades supports plugins, so no action taken. Metrics will be collected by the plugin instead.", file=sys.stderr)
        return

    timestamp = last_successful_run_timestamp()
    if timestamp is not None:
        reporting.report_last_successful_run_timestamp(timestamp)
        print("Info: metrics written to {}".format(
            reporting.OUTPUT_DIR), file=sys.stderr)


if __name__ == '__main__':
    main()
