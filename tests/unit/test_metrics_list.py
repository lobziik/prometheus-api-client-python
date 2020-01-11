import unittest
import datetime

import pytest

from prometheus_api_client import MetricsList


class TestMetricsList:
    @pytest.fixture(autouse=True)
    def setup(self, raw_metrics):
        self.raw_metrics_list = raw_metrics

    def test_init_single_metric(self):
        assert (
            len(MetricsList(self.raw_metrics_list[0][0])) is 1
        ), "incorrect number of Metric objects initialized for a raw metric not in a list"
        assert (
            len(MetricsList([self.raw_metrics_list[0][0]])) is 1
        ), "incorrect number of Metric objects initialized for a single metric list"

    def test_unique_metric_combination(self):
        start_time = datetime.datetime(2019, 7, 28, 10, 0)
        start_time_plus_1m = datetime.datetime(2019, 7, 28, 10, 1)
        end_time = datetime.datetime(2019, 7, 30, 10, 0)
        end_time_minus_1m = datetime.datetime(2019, 7, 30, 9, 59)

        assert (
            MetricsList(self.raw_metrics_list)[0].start_time > start_time,
            "Combined metric start time incorrect",
        )
        assert (
            MetricsList(self.raw_metrics_list)[0].start_time < start_time_plus_1m,
            "Combined metric start time incorrect",
        )
        assert (
            MetricsList(self.raw_metrics_list)[0].end_time < end_time,
            "Combined metric end time incorrect",
        )
        assert (
            MetricsList(self.raw_metrics_list)[0].end_time > end_time_minus_1m,
            "Combined metric end time incorrect",
        )
