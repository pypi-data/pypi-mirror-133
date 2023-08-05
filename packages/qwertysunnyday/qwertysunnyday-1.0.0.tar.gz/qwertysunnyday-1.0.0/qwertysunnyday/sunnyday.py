import requests

url = "http://api.openweathermap.org/data/2.5/forecast?q=Madrid&APPID=" \
      "bd6fd4c36eab2e7ac9a73498c7d97d66&units=imperial"
r = requests.get(url)
# print(r.json())

class Weather:
    """
    Creates a Weather bject getting an apikey as input
    and either a city name or lat and lon coordinates.

    Package use example:

    # Create a weather object using a city name:
    # The api key below is not guaranteed to work.
    # Get your own apikey from https://openweathermap.org
    # And wait a couple of hours for the apikey to be activated

    >>> weather1 = Weather(apikey = "bd6fd4c36eab2e7ac9a73498c7d97d66", city = "Madrid")

    # Using latitue and longitude coordinates
    >>> weather2 = Weather(apikey="bd6fd4c36eab2e7ac9a73498c7d97d66", lat=41.5, lon=10.15)

    # Get complete weather data for the next 12 hours:
    >>> weather1.next_12h()

    # Or simplified data with
    >>> weather1.next_12h_simplified()
    """

    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&" \
                  f"APPID={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&" \
                  f"APPID={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("Please provide either a city or lat and lon")

        if self.data["cod"] != "200":
            raise ValueError(self.data["message"])


    def next_12h(self):
        """
        Returns 3-hour data for the next 12 hours as a dictionary
        """
        return self.data['list'][:4]

    def next_12h_simplified(self):
        """
        Returns datetime, temperature and sky conditions for the next 12 hours as 3-hour intervals data
        """
        simple_data=[]
        for dicty in self.data['list'][0:4]:
            simple_data.append((dicty['dt_txt'], dicty['main']['temp'],
                                dicty['weather'][0]['description']))
        return simple_data


