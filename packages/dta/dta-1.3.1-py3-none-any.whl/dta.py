import sys

if sys.version_info[0] >= 3: # Python 3 or higher
	class __ConvertedDict(object):
		"""
		A class that handle the converting. (Suggest to use dta.Dict2Attr for easier uses)

		Initialize this class with dictionary
		"""
		
		def __init__(self, data):
			"""
			Conversion progress
			
			Keyword arguments:
				data -- Handle the dictionary
			Return: None
			"""
			
			for name, value in data.items():
				setattr(self, name, self._wrap(value))

		def _wrap(self, value):
			"""
			Wrapping the data to attributes
			
			Keyword arguments:
				value -- value that want to wrap
			Return: Return a __ConvertedDict class or type or value
			"""
			
			if isinstance(value, (tuple, list, set, frozenset)): 
				return type(value)([self._wrap(v) for v in value])
			else:
				return __ConvertedDict(value) if isinstance(value, dict) else value
	
	def Dict2Attr(data = None):
		"""
		Dictionary To Attributes function
		
		Keyword arguments:
			data -- The object you want to convert to class attributes. Worth knowing that you can't use any other than dictionary or have space in key
		Return: __ConvertedDict object or exceptions
		"""
		for name, value in data.items():
			if " " in name:
				raise ValueError("Attribute name cannot contain space: {}".format(name))
		if isinstance(data, dict):
			return __ConvertedDict(data)
		else:
			raise TypeError("Expected dict, got {}".format(type(data)))
else: # Python 2
	class __ConvertedDict(object):
		"""
		A class that handle the converting. (Suggest to use dta.Dict2Attr for easier uses)

		Initialize this class with dictionary
		"""
		def __init__(self, data):
			"""
			Conversion progress
			
			Keyword arguments:
				data -- Handle the dictionary
			Return: None
			"""
			for name, value in data.iteritems():
				setattr(self, name, self._wrap(value))

		def _wrap(self, value):
			"""
			Wrapping the data to attributes
			
			Keyword arguments:
				value -- value that want to wrap
			Return: Return a __ConvertedDict class or type or value
			"""
			if isinstance(value, (tuple, list, set, frozenset)): 
				return type(value)([self._wrap(v) for v in value])
			else:
				return __ConvertedDict(value) if isinstance(value, dict) else value
	def Dict2Attr(data = None):
		"""
		Dictionary To Attributes function
		
		Keyword arguments:
			data -- The object you want to convert to class attributes. Worth knowing that you can't use any other than dictionary or have space in key
		Return: __ConvertedDict object or exceptions
		"""
		for name, value in data.iteritems():
			if " " in name:
				raise ValueError("Attribute name cannot contain space: {}".format(name))
		return __ConvertedDict(data)

def Attr2Dict(data = None):
	"""
	Converting attributes back to normal dictionary

	Keyword arguments:
		data -- The __ConvertedDict object else you will get exception
	Return: Dictionary or exception
	"""
	if isinstance(data, __ConvertedDict):
		return data.__dict__
	else:
		raise TypeError("Expected __ConvertedDict, got {}".format(type(data)))

del sys

__all__ = {
	"Dict2Attr": Dict2Attr,
	"Attr2Dict": Attr2Dict,
	"__ConvertedDict": __ConvertedDict,
}
