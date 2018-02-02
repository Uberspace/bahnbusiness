import datetime

from pytest import fixture


@fixture
def api():
    from bahnbusiness import BahnApi
    return BahnApi()


@fixture
def authapi(api):
    api.login()
    return api


def test_login(api):
    api.login()


def test_get_journeys(authapi):
    from bahnbusiness import Journey

    j = authapi.get_journeys()
    j = list(j)

    assert len(j) > 0
    assert isinstance(j[0], Journey)
    assert isinstance(j[0].booking_date, datetime.date)
    assert isinstance(j[0].journey_date, datetime.date)
    assert len(j[0].name_travel) > 0


def test_get_url(authapi):
    from bahnbusiness import Journey

    j = next(authapi.get_journeys())
    url = authapi._get_ticket_url(j)

    assert isinstance(url, str)
    assert url.startswith('http')


def test_download(authapi):
    from bahnbusiness import Journey

    j = next(authapi.get_journeys())
    ticket = authapi.download_ticket(j)

    assert len(ticket) > 10000
