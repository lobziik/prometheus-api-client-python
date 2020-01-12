"""
Test module for class PrometheusConnect
"""
import os
from datetime import datetime, timedelta

import pytest

from prometheus_api_client import MetricsList, PrometheusConnect


pytestmark = pytest.mark.e2e


class TestPrometheusConnect:
    """
    Test module for class PrometheusConnect
    """

    @pytest.fixture(autouse=True)
    def setup(self):
        """
        set up connection settings for prometheus
        """
        self.prometheus_host = os.getenv("PROM_URL")
        self.pc = PrometheusConnect(url=self.prometheus_host, disable_ssl=True)

    def test_metrics_list(self):
        """
        Check if setup was done correctly
        """
        metrics_list = self.pc.all_metrics()
        assert len(metrics_list) > 0, "no metrics received from prometheus"

    def test_get_metric_range_data(self):
        start_time = datetime.now() - timedelta(minutes=10)
        end_time = datetime.now()
        metric_data = self.pc.get_metric_range_data(
            metric_name="up", start_time=start_time, end_time=end_time
        )

        metric_objects_list = MetricsList(metric_data)

        assert len(metric_objects_list) > 0, "no metrics received from prometheus"
        assert (
            start_time.timestamp() < metric_objects_list[0].start_time.timestamp(),
            "invalid metric start time",
        )
        assert (
            (start_time + timedelta(minutes=1)).timestamp()
            > metric_objects_list[0].start_time.timestamp(),
            "invalid metric start time",
        )
        assert (
            end_time.timestamp() > metric_objects_list[0].end_time.timestamp(),
            "invalid metric end time",
        )
        assert (
            (end_time - timedelta(minutes=1)).timestamp()
            < metric_objects_list[0].end_time.timestamp(),
            "invalid metric end time",
        )

    def test_get_metric_range_data_with_chunk_size(self):
        start_time = datetime.now() - timedelta(minutes=65)
        chunk_size = timedelta(minutes=7)
        end_time = datetime.now() - timedelta(minutes=5)
        metric_data = self.pc.get_metric_range_data(
            metric_name="up", start_time=start_time, end_time=end_time, chunk_size=chunk_size
        )

        metric_objects_list = MetricsList(metric_data)

        assert len(metric_objects_list) > 0, "no metrics received from prometheus"
        assert (
            start_time.timestamp() < metric_objects_list[0].start_time.timestamp(),
            "invalid metric start time (with given chunk_size)",
        )
        assert (
            (start_time + timedelta(minutes=1)).timestamp()
            > metric_objects_list[0].start_time.timestamp(),
            "invalid metric start time (with given chunk_size)",
        )
        assert (
            end_time.timestamp() > metric_objects_list[0].end_time.timestamp(),
            "invalid metric end time (with given chunk_size)",
        )
        assert (
            (end_time - timedelta(minutes=1)).timestamp()
            < metric_objects_list[0].end_time.timestamp(),
            "invalid metric end time (with given chunk_size)",
        )
