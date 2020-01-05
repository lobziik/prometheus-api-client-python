import pytest
import requests

from prometheus_api_client.prometheus_connect import PrometheusConnect
from prometheus_api_client.exceptions import PrometheusApiClientException

from .prom_responses import ALL_METRICS


def test_network_blocked():
    """
    For documenting purposes, keep in mind that all network interactions blocked in this module
    """
    resp = requests.get("http://some-url-there.org")
    assert resp.content == b"BOOM!"
    assert resp.status_code == 403


class TestPrometheusConnect:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.pc = PrometheusConnect(url="http://mocked-host.org")

    def test_unauthorized(self, mocked_response):
        with mocked_response("Unauthorized", status_code=403):
            with pytest.raises(PrometheusApiClientException) as exc:
                self.pc.all_metrics()
        assert "HTTP Status Code 403 (b'Unauthorized')" in str(exc)

    def test_all_metrics(self, mocked_response):
        with mocked_response(ALL_METRICS) as handler:
            assert len(self.pc.all_metrics())
            assert handler.call_count == 1
            request = handler.requests[0]
            assert request.path_url == '/api/v1/label/__name__/values'
