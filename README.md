# geopop
Python library for getting populations size given a place name

```python
>> gp = GeoPop()
>> gp.population("Moscow", 30)
>> 14029857
```

This library works in a bold way: on initialization it loads into memory all data that resides in the data directory specified by the user or data included by default in the "data" directory. When a 'population' method is called it simply scans through all the data points and sums the population for those that appear to be in the specified radius.

Performance improvments:
  * search only in the country-specific subset of data
  * sort datapoints by lat/lon for faster search
  * use rtree/sqlite to index the data

