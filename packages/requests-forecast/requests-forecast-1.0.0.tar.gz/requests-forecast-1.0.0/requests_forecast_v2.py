import pytz
import requests
import time as time_mod

from datetime import datetime


__title__ = "requests-forecast"
__version__ = "0.6.2"
__author__ = "Jeff Triplett"
__license__ = "BSD"
__copyright__ = "Copyright 2013-2016 Jeff Triplett"


DARKSKY_TEMPLATE_URI = (
    "https://api.darksky.net/forecast/{key}/{latitude},{longitude}{time}"
)

DEFAULT_HEADERS = {
    "Accept-Encoding": "gzip",
}

DEFAULT_TIMEZONE = "America/New_York"

ALERT_FIELDS = ("alerts",)

DATA_FIELDS = ("data",)

DECIMAL_FIELDS = (
    "cloudCover",
    "precipProbability",
    "humidity",
)

TIME_FIELDS = (
    "expires",
    "time",
)

"""

Data Point Object

Data Block Object

Alerts Array

Flags Object

"""


class DataBlock(dict):
    def __init__(self, data=None, timezone=None):
        self.timezone = str(timezone)
        if data:
            for key in data.keys():
                if key in DATA_FIELDS:
                    self.data = []
                    print(key)
                    print(data[key])
                    for datapoint in data[key]:
                        self.data.append(DataPoint(data=datapoint, timezone=timezone))

            super().__init__(data)

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

    def __repr__(self):
        return "<DataBlock summary={}>".format(self["summary"])


class DataPoint(dict):
    def __init__(self, data=None, timezone=None):
        self.timezone = str(timezone)
        if data:
            for key in data.keys():
                if key in ALERT_FIELDS:
                    self.alerts = []
                    for alert in data[key]:
                        self.alerts.append(DataPoint(data=alert, timezone=timezone))

                elif key in DATA_FIELDS:
                    self.data = []
                    for datapoint in data[key]:
                        print(datapoint)
                        obj = DataPoint(data=datapoint, timezone=timezone)
                        print(obj)
                        self.data.append(obj)

                elif key in DECIMAL_FIELDS:
                    data[key] = float(data[key]) * float("100.0")

                elif key in TIME_FIELDS or key.endswith("Time"):
                    if timezone:
                        tz = pytz.timezone(str(timezone))
                        utc = pytz.utc
                        ts = datetime.utcfromtimestamp(int(data[key])).replace(
                            tzinfo=utc
                        )
                        data[key] = tz.normalize(ts.astimezone(tz))
                    else:
                        data[key] = datetime.fromtimestamp(int(data[key]))

            super().__init__(data)

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr)

    def __repr__(self):
        if "summary" in self:
            return f"<DataPoint summary={self.summary}>"
        else:
            print(self.precipProbability)
            print(self.time)
            print(self.precipIntensity)
            return "<DataPoint {0}>"  # .format(self)


class ParsedAlert:
    def __init__(self, parser):
        super().__init__()
        self._parser = parser

    @classmethod
    def from_dict(klass, d, parser):

        # The new ParsedArticle.
        p = klass(parser=parser)

        # Add all values from returned JSON object to instance.
        for key, value in d.iteritems():
            setattr(p, key, value)

        # Update Datetimes...

        return p


class ParsedCurrently:
    def __init__(self, parser):
        super().__init__()
        self._parser = parser


class ParsedDaily:
    def __init__(self, parser):
        super().__init__()
        self._parser = parser


class ParsedHourly:
    def __init__(self, parser):
        super().__init__()
        self._parser = parser


class ParsedMinutely:
    def __init__(self, parser):
        super().__init__()
        self._parser = parser


class Forecast:
    json = None
    timezone = None

    def __init__(
        self, apikey, latitude=None, longitude=None, timezone=None, time=None, **kwargs
    ):
        self.apikey = apikey
        self.latitude = latitude
        self.longitude = longitude

        # self.timezone = timezone

        self.time = time

        """
        TODO: exclude=[blocks]
        TODO: extend=hourly
        TODO: lang=[language]
        """

        self.exclude = kwargs.get("exclude", None)
        self.extend = kwargs.get("extend", None)
        self.lang = kwargs.get("lang", "en")
        self.units = kwargs.get("units", "auto")

        if not self.apikey:
            raise ValueError("No API key is set")

        self.fetch()

    @property
    def params(self):
        return {
            "exclude": self.exclude,
            "extend": self.extend,
            "lang": self.lang,
            "units": self.units,
        }

    def fetch(self, latitude=None, longitude=None, time=None, units=None):
        if time:
            time = int(time_mod.mktime(time.timetuple()))

        url = DARKSKY_TEMPLATE_URI.format(
            key=self.apikey,
            latitude=latitude or self.latitude,
            longitude=longitude or self.longitude,
            time=f",{time}" if self.time else "",
        )

        request = requests.get(url, headers=DEFAULT_HEADERS, params=self.params)

        request.raise_for_status()

        self.forecast = request.json()

        return self.forecast

    @property
    def alerts(self):
        if "alerts" in self.forecast:
            alerts = []
            for alert in self.forecast["alerts"]:
                alerts.append(DataPoint(alert, self.timezone))
            return alerts
        else:
            return DataPoint()

    @property
    def currently(self):
        if "currently" in self.forecast:
            return DataPoint(self.forecast["currently"], self.timezone)
        else:
            return DataPoint()

    @property
    def daily(self):
        if "daily" in self.forecast:
            return DataPoint(self.forecast["daily"], self.timezone)
        else:
            return DataPoint()

    @property
    def hourly(self):
        if "hourly" in self.forecast:
            return DataPoint(self.forecast["hourly"], self.timezone)
        else:
            return DataPoint()

    @property
    def minutely(self):
        if "minutely" in self.forecast:
            return DataPoint(self.forecast["minutely"], self.timezone)
        else:
            return DataPoint()

    """
    @property
    def offset(self):
        if 'offset' in self.forecast:
            return self.forecast['offset']
        return None
    """

    @property
    def timezone(self):
        if "timezone" in self.forecast:
            return pytz.timezone(self.forecast["timezone"])
        else:
            return None


# Alert Array
def alerts(
    apikey=None, latitude=None, longitude=None, timezone=None, units=None, time=None
):
    fore = Forecast(
        apikey=apikey,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        time=time,
        units=units,
    )
    return fore.alerts


# Data Point
def currently(
    apikey=None, latitude=None, longitude=None, timezone=None, units=None, time=None
):
    fore = Forecast(
        apikey=apikey,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        time=time,
        units=units,
    )
    return fore.currently


# Data Block
def daily(
    apikey=None, latitude=None, longitude=None, timezone=None, units=None, time=None
):
    fore = Forecast(
        apikey=apikey,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        time=time,
        units=units,
    )
    return fore.daily


# Data Block
def hourly(
    apikey=None, latitude=None, longitude=None, timezone=None, units=None, time=None
):
    fore = Forecast(
        apikey=apikey,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        time=time,
        units=units,
    )
    return fore.hourly


# Data Block
def minutely(
    apikey=None, latitude=None, longitude=None, timezone=None, units=None, time=None
):
    fore = Forecast(
        apikey=apikey,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        time=time,
        units=units,
    )
    return fore.minutely
