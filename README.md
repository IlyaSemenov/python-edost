# python-edost

This is a simple set of Python bindings for edost.ru, a Russian delivery cost calculation service.

## Installation

    pip install edost

## Usage

Get the list of tariffs:

```python
import edost
	
edost_client = edost.EdostClient('<client id>', '<password>')
tariffs = edost_client.get_tariffs(
	to_city=edost.EDOST_ID_FOR_CITY[u'Новосибирск'],
	weight=1,
	strah=1000,
)

print tariffs[0]  # {'price': 210.0, 'delivery_time': u'', 'company': u'PONY EXPRESS', 'id': 27, 'name': None}
```

Construct the city selector:

```python
import edost
from django.db import models

CITY_CHOICES = [(city_code, full_city) for city_code, city, region, full_city in edost.EDOST_CITIES]
city_code = models.PositiveIntegerField(choices=CITY_CHOICES)
```