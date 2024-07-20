import os
import sys
from pathlib import Path

OUTPUT_DIR = os.getenv('OUTPUT_DIR', '/var/lib/prometheus/node-exporter')


def report_last_successful_run_timestamp(timestamp):
    io, transaction = atomic_open_output(
        'unattended-upgrades-last-successful-run-timestamp.prom')
    try:
        io.write(
            '# HELP unattended_upgrades_last_successful_run_timestamp Timestamp of the last unattended-upgrades successful run\n')
        io.write(
            '# TYPE unattended_upgrades_last_successful_run_timestamp gauge\n')
        io.write(
            'unattended_upgrades_last_successful_run_timestamp {}\n'.format(timestamp))
    finally:
        atomic_end_output(io, transaction)
    atomic_commit_output(transaction)


def report_last_failed_run_timestamp(timestamp):
    io, transaction = atomic_open_output(
        'unattended-upgrades-last-failed-run-timestamp.prom')
    try:
        io.write(
            '# HELP unattended_upgrades_last_failed_run_timestamp Timestamp of the last unattended-upgrades failed run\n')
        io.write(
            '# TYPE unattended_upgrades_last_failed_run_timestamp gauge\n')
        io.write(
            'unattended_upgrades_last_failed_run_timestamp {}\n'.format(timestamp))
    finally:
        atomic_end_output(io, transaction)
    atomic_commit_output(transaction)


def atomic_open_output(basename):
    if OUTPUT_DIR in ['-', '/dev/stdout']:
        return (sys.stdout, None)
    else:
        temp_output_path = Path(OUTPUT_DIR) / (basename + '.tmp')
        return (temp_output_path.open('w', encoding='UTF-8'), (temp_output_path, basename))


def atomic_end_output(io, transaction):
    if transaction is not None:
        io.close()


def atomic_commit_output(transaction):
    if transaction is not None:
        temp_output_path, basename = transaction
        temp_output_path.rename(Path(OUTPUT_DIR) / basename)
