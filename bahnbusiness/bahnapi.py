import configparser
import os

from bs4 import BeautifulSoup
import requests

from .journey import Journey


class BahnApi:
  BASE_URL = "https://fahrkarten.bahn.de/grosskunde"
  LOGIN_URL = BASE_URL + "/start/kmu_start.post?scope=login"
  JOURNEY_LIST = BASE_URL + "/buchungsrueckschau/brs_uebersicht.go?brsmode=3"
  JOURNEY_SEARCH_POST = BASE_URL + "/buchungsrueckschau/brs_auftrag_suche.post"
  JOURNEY_DETAILS = BASE_URL + "/buchungsrueckschau/brs_auftrag_details.post"

  def __init__(self):
    self._session = requests.session()
    self._csrf_token = None
    self._click_id = None

  @classmethod
  def _get_config(cls):
    config = configparser.ConfigParser()
    config.read(['.bahnbusiness-login', os.path.expanduser('~/.bahnbusiness-login')])

    try:
      return dict(config.items('bahnbusiness'))
    except configparser.NoSectionError:
      return {'username': None, 'password': None}

  def _get_and_parse(self, url, **kwargs):
    """
    Perform a HTTP request on the given url using requests and return the response BeautifulSoup.
    Also echo back any click_id or csrf_token values found in the last response
    """
    kwargs = kwargs.copy()
    kwargs.setdefault('method', 'GET')

    if 'data' in kwargs:
      if self._csrf_token:
        kwargs['data'].setdefault('csrf_token', self._csrf_token)
      if self._click_id:
        kwargs['data'].setdefault('click_id', self._click_id)

    r  = self._session.request(url=url, **kwargs)
    soup = BeautifulSoup(r.text, 'html.parser')

    self._click_id = soup.select('[name=click_id]')[0]['value']
    self._csrf_token = soup.select('[name=csrf_token]')[0]['value']

    return soup

  def login(self, username=None, password=None):
    """
    Try to login via the provided credentials or the ones in .bahnbusiness-login.
    The resulting login-session is valid for all further requests using this BahnApi-instance.
    """
    if not username:
      username = self._get_config()['username']
    if not password:
      password = self._get_config()['password']

    if not username:
      raise Exception('No username provided')
    if not password:
      raise Exception('No password provided')

    r = self._get_and_parse(self.LOGIN_URL,
      method='POST',
      data={
        'lang': 'de',
        'country': 'DE',
        'username': username,
        'password': password,
      }
    )

    if not bool(r(text='Meine Daten verwalten')):
      raise Exception('Login failed')

  def get_journeys(self):
    html = self._get_and_parse(self.JOURNEY_LIST)

    for row in html.select('.brsoverviewtable2 tr')[1:]:
      fields = [f.text.strip() for f in row.select('td')]

      if len(fields) > 1:  # first row is always empty
        yield Journey(*fields)

  def _get_ticket_url(self, journey):
    self._get_and_parse(self.JOURNEY_SEARCH_POST,
      method='POST',
      data={
        'auftragsnr': journey.id,
        'reisenderNachname': journey.name_travel,
        'button.suchen_p_js': 'true',
      }
    )

    if journey.description == 'BahnCard':
      html = self._get_and_parse(self.JOURNEY_DETAILS,
        method='POST',
        data={
          'button.kaufbelegAnfordern_p_js': 'true',
        }
      )

      try:
        return html.select('a.arrowlink')[0]['href']
      except:
        raise Exception('Could not find invoice URL for {}'.format(journey.id))
    else:
      html = self._get_and_parse(self.JOURNEY_DETAILS,
        method='POST',
        data={
          'button.bahnfahrtAbrufen_p_js': 'true',
          'button.reservierungabrufen_p_js': 'true',
        }
      )

      try:
        return html.select('a.btn')[0]['href']
      except:
        raise Exception('Could not find ticket URL for {}'.format(journey.id))

  def download_ticket(self, journey):
    """ Get the ticket for the given journey as bytes() """

    url = self._get_ticket_url(journey)
    r = self._session.get(url, stream=True)
    return r.raw.read()
