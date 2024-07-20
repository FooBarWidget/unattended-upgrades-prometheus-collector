#!/usr/bin/env python3
import importlib
plugin = importlib.import_module('unattended-upgrades-prometheus-collector')


class Result:
    def __init__(self, success):
        self.success = success


plugin.StatsPlugin().postrun(Result(True))
plugin.StatsPlugin().postrun(Result(False))
