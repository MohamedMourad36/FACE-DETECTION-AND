"""utilities"""
from .encoder import Encoder
import face_recognition as fr
from .datastore import attendence
import csv

def get_id(encode):
	store = Encoder.get_encodes()

	for k, v in store.items():
		res = fr.compare_faces([v], encode, tolerance=0.45)
		if not res:
			continue
		if res[0]==True:
			return True, k
	return False, None


def get_attendence():
	"""Return attendence"""
	return attendence