"""GUI Help"""
from datetime import datetime
from tkinter import *
from tkinter import ttk, filedialog
import face_recognition as fr
from .datastore import attendence
from .utils import get_id


class Draw:
	"""draw window objects"""

	@staticmethod
	def get_img_faces_dialog():
		"""get img path"""
		file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
		if not file_path:
			return

		image = fr.load_image_file(file_path)
		face_encodings = fr.face_encodings(image)
		for face_encoding in face_encodings:
			sid = get_id(face_encoding)
			now = datetime.now().strftime('%H:%M:%S')
			# setattr(attendence, f"{sid}", now)
			attendence[f"{sid}"] = now