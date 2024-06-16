"""Get the encodings"""
import os
from .datastore import storage
import face_recognition as fr
import cv2 as cv
import numpy as np

class Encoder:
	"""Encoder class"""

	@staticmethod
	def store_encodes(dir):
		"""Store the images encodings from a directory"""
		for img in os.listdir(dir):
			sp_img = os.path.splitext(img)

			if sp_img[0] == 'test' or \
				sp_img[1] not in ('.jpg', '.jpeg', '.png'):
				continue

			cimg = cv.imread(f"{dir}/{img}")
			cimg = cv.cvtColor(cimg, cv.COLOR_BGR2RGB)

			encode = fr.face_encodings(cimg)
			if encode:
				storage.new(sp_img[0], encode[0])

	@staticmethod
	def get_encodes():
		"""Returns the encodings dict"""
		return storage.all()