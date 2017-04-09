__author__ = 'nyddle'

import unittest

from geopop import GeoPop
from geopop.exceptions import *

class TestGeoPop(unittest.TestCase):

    def test_no_data(self):

        with self.assertRaises(NoGeodata):
            GeoPop(data_dir='tests')


    def test_wrong_location(self):

        with self.assertRaises(LocationNotFound):

            gp = GeoPop(data_dir='tests/data')
            gp.population('dsvsdvjdsvkjsd', 30)


    def test_bedrock_population(self):

        gp = GeoPop(data_dir='tests/data')
        self.assertEqual(gp.population('Bedrock', 50), 98926)


if __name__ == '__main__':
    unittest.main()