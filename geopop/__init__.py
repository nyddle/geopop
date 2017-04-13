__author__ = 'nyddle'

import os

from geopy.distance import vincenty
import glob

from collections import namedtuple, defaultdict

from .exceptions import NoGeodata, LocationNotFound

header = ('geonameid', 'name', 'asciiname', 'alternatenames', 'latitude',
          'longitude', 'feature_class', 'feature_code', 'country_code', 'cc2',
          'a1', 'a2', 'a3', 'a4', 'population', 'elevation', 'dem', 'timezone',
          'modification_date')

Location = namedtuple('Location', header)


class GeoPop(object):
    """
    GeoPop is an interface for querying data from
    geonames.org dataset
    """

    def available_countries(self):

        return list(filter(lambda x: x.endswith(('.txt', )),
                      os.listdir(self.data_dir)))

    def location(self, name):

        return self.locations.get(name.lower(), None)

    def population(self, name: str, proximity: int) -> int:
        """

        :param name: location name, e.g. Moscow
        :param proximity: the great circle radius
        :return: population inside the great circle of a given location/proximity
        """

        population = 0

        if name.lower() not in self.locations:
            raise LocationNotFound

        location = self.locations[name.lower()]
        print(location)
        for loc in self.geo_data[location.country_code]:

            distance = vincenty((location.latitude, location.longitude),
                                (loc.latitude, loc.longitude)).kilometers
            #print(distance)
            if distance > proximity:
                continue
            #else:
            #    print(loc)

            population += int(loc.population)

        return population

    def __init__(self, data_dir=None):

        self.data_dir = data_dir or os.path.join(
            os.path.dirname(__file__), '../data')
        self.geo_data = defaultdict(list)
        self.locations = {}

        if not self.available_countries():
            raise NoGeodata

        for country_data in glob.glob(os.path.join(self.data_dir, '*.txt')):
            with open(country_data) as geo_data:
                for line in geo_data:
                    loc = Location(*line.split("\t"))
                    self.locations[loc.name.lower()] = loc
                    if loc.population == '0':
                        continue
                    self.geo_data[loc.country_code].append(loc)
