import datetime


class Journey:
  """ Represents a single journey (e.g. A and B traveling from Berlin to Hamburg on 2018-01-15) """

  @classmethod
  def _parse_date(cls, date):
    return datetime.datetime.strptime(date, "%d.%m.%Y").date()

  def __init__(self, id, booking_date, name_booking, journey_date, name_travel, description, route, *args):
    self.id = id
    self.booking_date = self._parse_date(booking_date)
    self.name_booking = name_booking
    self.journey_date = self._parse_date(journey_date)
    self.name_travel = name_travel
    self.description = description
    self.route = route
