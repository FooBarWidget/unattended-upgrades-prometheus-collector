import time
import reporting


class StatsPlugin:
    def postrun(self, result):
        if result.success:
            reporting.report_last_successful_run_timestamp(int(time.time()))
        else:
            reporting.report_last_successful_run_timestamp(int(time.time()))
