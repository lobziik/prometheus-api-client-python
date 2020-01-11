"""unit tests for Metrics Class."""
import datetime
import pytest

from prometheus_api_client import Metric


class TestMetric:
    """unit tests for Metrics Class."""

    @pytest.fixture(autouse=True)
    def setup(self, raw_metrics):
        self.raw_metrics_list = raw_metrics

    def test_init(self):
        test_metric_object = Metric(self.raw_metrics_list[0][0])
        assert test_metric_object.metric_name == "up", "incorrect metric name"

    def test_init_errors(self):
        with pytest.raises(
            TypeError,
            match="oldest_data_datetime can only be datetime.datetime/ datetime.timedelta",
        ):
            Metric(self.raw_metrics_list[0][0], oldest_data_datetime="2d")

    def test_metric_start_time(self):
        start_time = datetime.datetime(2019, 7, 28, 10, 0)
        start_time_plus_1m = datetime.datetime(2019, 7, 28, 10, 1)

        test_metric_object = Metric(self.raw_metrics_list[0][0])
        assert test_metric_object.start_time > start_time, "incorrect metric start time"
        assert test_metric_object.start_time < start_time_plus_1m, "incorrect metric start time"

    def test_metric_end_time(self):
        end_time = datetime.datetime(2019, 7, 28, 16, 00)
        end_time_minus_1m = datetime.datetime(2019, 7, 28, 15, 59)

        test_metric_object = Metric(self.raw_metrics_list[0][0])
        assert test_metric_object.end_time > end_time_minus_1m, "incorrect metric end time"
        assert test_metric_object.end_time < end_time, "incorrect metric end time"

    def test_metric_equality(self):
        assert Metric(self.raw_metrics_list[0][0]) == Metric(self.raw_metrics_list[1][0])
        assert Metric(self.raw_metrics_list[0][0]) != Metric(self.raw_metrics_list[0][1])

    def test_addition_errors(self):
        with pytest.raises(TypeError, match="Different metric labels"):
            Metric(self.raw_metrics_list[0][0]) + Metric(self.raw_metrics_list[0][1])

    def test_metric_addition(self):
        sum_metric = Metric(self.raw_metrics_list[0][0]) + Metric(self.raw_metrics_list[1][0])
        assert isinstance(sum_metric, Metric), "The sum is not a Metric"
        assert (
            sum_metric.start_time == Metric(self.raw_metrics_list[0][0]).start_time
        ), "Incorrect Start time after addition"
        assert (
            sum_metric.end_time == Metric(self.raw_metrics_list[1][0]).end_time
        ), "Incorrect End time after addition"

    def test_oldest_data_datetime_with_datetime(self):
        expected_start_time = Metric(self.raw_metrics_list[0][0]).metric_values.iloc[4, 0]
        new_metric = Metric(
            self.raw_metrics_list[0][0], oldest_data_datetime=expected_start_time
        ) + Metric(self.raw_metrics_list[1][0])

        assert expected_start_time == new_metric.start_time, "Incorrect Start time after addition"
        assert (
            expected_start_time == new_metric.metric_values.iloc[0, 0]
        ), "Incorrect Start time after addition (in df)"

    def test_oldest_data_datetime_with_timedelta(self):
        expected_start_time = Metric(self.raw_metrics_list[0][0]).metric_values.iloc[4, 0]
        time_delta = (
            Metric(self.raw_metrics_list[1][0]).metric_values.iloc[-1, 0]
            - Metric(self.raw_metrics_list[0][0]).metric_values.iloc[4, 0]
        )
        new_metric = Metric(self.raw_metrics_list[0][0], oldest_data_datetime=time_delta) + Metric(
            self.raw_metrics_list[1][0]
        )
        assert expected_start_time == new_metric.start_time, "Incorrect Start time after addition"
