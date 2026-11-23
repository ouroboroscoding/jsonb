# JSON Better
[![pypi version](https://img.shields.io/pypi/v/jsonb.svg)](https://pypi.org/project/jsonb)
![MIT License](https://img.shields.io/pypi/l/jsonb.svg)

A Python library used to simplify encoding/decoding JSON while handling special
types such as `Decimal` and `datetime`.

Please see [LICENSE](https://github.com/ouroboroscoding/jsonb/blob/main/LICENSE)
for further information.

See [Releases](https://github.com/ouroboroscoding/jsonb/blob/main/releases.md)
for changes from release to release.

## Requires
jsonb requires python 3.10 or higher

## Installation
```bash
pip install jsonb
```

## Usage

```python
import jsonb
from decimal import Decimal
from datetime import datetime

# Encode special types
s = jsonb.encode({
	'amount': Decimal('12.50'),
	'when': datetime(2023, 3, 15, 12, 0, 0)
})

# Decode floats as Decimal by default
data = jsonb.decode('{"amount": 12.50}')
# data['amount'] is Decimal('12.5')

# Pass additional arguments through to the json module
s = jsonb.encode(data, indent=2, sort_keys=True)
data = jsonb.decode(s, parse_int=Decimal)
```

### File helpers

```python
import jsonb

# Load / store by path (~ is expanded)
data = jsonb.load('~/config.json')
jsonb.store(data, '~/config.json', indent=2)

# Or work with open file objects
with open('data.json', 'r') as f:
	data = jsonb.decodef(f)

with open('data.json', 'w') as f:
	jsonb.encodef(data, f, indent=2)
```

### Custom types

```python
import jsonb

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

jsonb.add_class(Point, lambda p: {'x': p.x, 'y': p.y})
print(jsonb.encode(Point(1, 2)))
```