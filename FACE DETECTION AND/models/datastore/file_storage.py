"""Handles Json files"""
import json
import numpy as np

class FileStorage:
	""" serializes/deserializes instances from/to a JSON file"""

	__file_path = "db.json"
	__objects = {}

	def all(self):
		"""Return the dictionary __objects."""
		return FileStorage.__objects

	def new(self, id, encoded):
		"""Set in __objects obj with key <obj_class_name>.id"""
		FileStorage.__objects[f"{id}"] = encoded

	def save(self):
		"""Serialize __objects to the JSON file __file_path."""
		odict = FileStorage.__objects
		objdict = {
			obj: odict[obj].tolist() for obj in odict.keys()
			}
		with open(FileStorage.__file_path, "w") as f:
			json.dump(objdict, f)

	def reload(self):
		"""Deserialize the JSON file __file_path to __objects, if it exists."""
		try:
			with open(FileStorage.__file_path) as f:
				for id, encoded in json.load(f).items():
					self.new(id, np.array(encoded))
		except FileNotFoundError:
			return