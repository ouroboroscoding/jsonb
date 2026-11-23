# coding=utf8
"""JSON Better

Wrapper for Python json module which handles custom types
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-03-15"

# Python modules
import json
from datetime import datetime
from decimal import Decimal
import os

def add_class(constructor: callable, callback: callable):
	"""Add Class

	Allows adding a class to be processed by a special callback

	Arguments
		constructor (type): The class to be processed by the callback
		callback (function): The callback to pass instances of the class

	Returns:
		None
	"""
	__Encoder.add_class(constructor, callback)

def decode(s: str, **kwargs):
	"""Decode

	Handles decoding JSON, as a string, into objects/values

	Args:
		s (str): The JSON to decode
		**kwargs: Additional arguments passed to json.loads. parse_float
			defaults to Decimal if not provided.

	Returns:
		mixed
	"""
	kwargs.setdefault('parse_float', Decimal)
	return json.loads(s, **kwargs)

def decodef(f, **kwargs):
	"""Decode File

	Handles decoding JSON, from a file, into objects/values

	Args:
		f (_io.TextIOWrapper): An instance of a file object with read/write
			methods
		**kwargs: Additional arguments passed to json.load. parse_float
			defaults to Decimal if not provided.

	Returns:
		mixed
	"""
	kwargs.setdefault('parse_float', Decimal)
	return json.load(f, **kwargs)

def encode(o: any, indent = None, **kwargs):
	"""Encode

	Handles encoding objects/values into a JSON string

	Args:
		o (any): The object or value to encode
		indent: Indentation level passed to json.dumps
		**kwargs: Additional arguments passed to json.dumps. cls defaults to
			the jsonb encoder if not provided.

	Returns:
		str
	"""
	kwargs.setdefault('cls', __Encoder)
	if 'indent' not in kwargs:
		kwargs['indent'] = indent
	return json.dumps(o, **kwargs)

def encodef(o, f, indent=None, **kwargs):
	"""Encode File

	Handles encoding objects/values into JSON and storing them in the given file

	Args:
		o (mixed): The object or value to encode
		f (_io.TextIOWrapper): An instance of a file object with read/write
			methods
		indent: Indentation level passed to json.dump
		**kwargs: Additional arguments passed to json.dump. cls defaults to
			the jsonb encoder if not provided.

	Returns:
		None
	"""
	kwargs.setdefault('cls', __Encoder)
	if 'indent' not in kwargs:
		kwargs['indent'] = indent
	return json.dump(o, f, **kwargs)

# load function
def load(filepath, **kwargs):
	"""Load

	Loads a data structure from a JSON file given a full or relative path to it

	Args:
		filepath (str): The path to the file to load
		**kwargs: Additional arguments passed to decode / json.loads

	Returns:
		mixed
	"""

	# If ~ is present
	if '~' in filepath:
		filepath = os.path.expanduser(filepath)

	# Load the file
	with open(filepath, 'r') as oFile:

		# Convert it to a python variable and return it
		return decode(oFile.read(), **kwargs)

# store function
def store(data, filepath, indent=None, **kwargs):
	"""Store

	Converts an object/value into JSON and stores it in the file path given

	Args:
		data: The object or value to encode
		filepath (str): The full or relative path to the file
		indent: Indentation level passed to encode / json.dumps
		**kwargs: Additional arguments passed to encode / json.dumps

	Returns:
		None
	"""

	# If ~ is present
	if '~' in filepath:
		filepath = os.path.expanduser(filepath)

	# Open a file to write the data
	with open(filepath, 'w') as oFile:

		# Write the JSON to the file
		oFile.write(encode(data, indent, **kwargs))

class __Encoder(json.JSONEncoder):
	"""Encoder

	Handles encoding types the default JSON encoder can't handle

	"""

	__classes = {
		datetime: lambda x: x.strftime('%Y-%m-%d %H:%M:%S'),
		Decimal: lambda x: '{0:f}'.format(x)
	}
	"""Classes

	Maps types to callbacks used when the default JSON encoder cannot
	handle a value. Lookup walks the instance's MRO so the most specific
	registered type wins."""

	@classmethod
	def add_class(cls, constructor: callable, callback: callable):
		"""Add Class

		Allows adding a class to be processed by a special callback

		Arguments
			constructor (type): The class to be processed by the callback
			callback (function): The callback to pass instances of the class

		Returns:
			None
		"""

		# Register / replace the handler for this exact type
		cls.__classes[constructor] = callback

	# default method
	def default(self, obj):
		"""Default

		Called when the regular Encoder can't figure out what to do with the
		type

		Args:
			obj (mixed): An unknown object or value that needs to be encoded

		Returns:
			str
		"""

		# Walk the MRO so a subclass handler beats a registered parent
		for oClass in type(obj).__mro__:
			if oClass in self.__classes:
				return self.__classes[oClass](obj)

		# Bubble back up to the parent default
		return json.JSONEncoder.default(self, obj)