__author__ = 'nyddle'

import os

from geopy.distance import vincenty
import glob

from collections import namedtuple


header = ('geonameid', 'name', 'asciiname', 'alternatenames', 'latitude', 'longitude', 'feature_class',
          'feature_code', 'country_code', 'cc2', 'a1', 'a2', 'a3', 'a4', 'population', 'elevation',
          'dem', 'timezone', 'modification_date')

Location = namedtuple('Location', header, verbose=True)

class LocationNotFound(Exception):
    pass

class GeoPop(object):
    """
    GeoPop is an interface for querying data from
    geonames.org dataset
    """

    def available_countries(self):

        return filter(lambda x: x.endswith(('.txt',)),
                      os.listdir(self.data_dir))

    def location(self, name):

        return self.locations.get(name.lower(), None)

    def population(self, name, proximity):
        """

        :param name: location name, e.g. Moscow
        :param proximity: the great circle radius
        :return: population inside the great circle of a given location/proximity
        """

        population = 0

        if name.lower() not in self.locations:
            raise LocationNotFound

        location = self.locations[name.lower()]

        for loc in self.geo_data:

            distance = vincenty((location.latitude, location.longitude),
                                (loc.latitude, loc.longitude)).miles

            if distance > proximity:
                continue

            population += int(loc.population)

        return population


    def __init__(self, data_dir='./data'):

        self.data_dir = data_dir
        self.geo_data = []
        self.locations = {}

        for country_data in glob.glob(os.path.join(self.data_dir, '*.txt')):
            with open(country_data) as geo_data:
                for line in geo_data:
                    loc = Location(*line.split("\t"))
                    self.geo_data.append(loc)
                    self.locations[loc.name.lower()] = loc
