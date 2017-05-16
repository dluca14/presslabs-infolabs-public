import pytest
import responses
from datetime import timedelta
from requests import Timeout

from domainCheck.crawlers.Domain import DomainCrawler


@responses.activate
def test_response_time_feature():
    dc = DomainCrawler()
    base_url = 'http://presslabs.com'
    responses.add(responses.GET, base_url, status=200)
    dc.crawl(base_url)
    res_list = dc.get_results_list()
    assert len(res_list) == len(dc.FEATURES_LIST)
    assert res_list[0].get_value() <= timedelta(microseconds=500)


@responses.activate
def test_response_time_feature_timeout():
    dc = DomainCrawler()
    base_url = 'http://presslabs.com'

    def request_callback(request):
        raise Timeout()

    responses.add_callback(
        responses.GET, base_url,
        callback=request_callback
    )

    dc.crawl(base_url)
    res_list = dc.get_results_list()
    assert res_list == []


@responses.activate
def test_response_time_404():
    dc = DomainCrawler()
    base_url = 'http://presslabs.com'
    responses.add(responses.GET, base_url, status=404)
    dc.crawl(base_url)
    res_list = dc.get_results_list()
    assert res_list == []