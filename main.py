from models.datastore import storage
from models.encoder import Encoder
from datetime import datetime, date
from tkinter import *
from tkinter import ttk, filedialog, messagebox
import csv
import face_recognition as fr
import cv2
from models.datastore import attendence
from models.utils import get_attendence, get_id

class HandleBoard:
    """Handle Window"""

    @staticmethod
    def get_past(date_str=None, show_error=True):
        attendence.clear()
        try:
            dt = date.today() if not date_str else datetime.strptime(date_str, '%Y-%m-%d').date()
            with open(f'{dt}.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    attendence[row['ID']] = row['Time']
        except FileNotFoundError:
            if show_error:
                messagebox.showerror("File Not Found", f"No attendance record found for {dt}")
        except ValueError:
            if show_error:
                messagebox.showerror("Invalid Date", "Please enter the date in YYYY-MM-DD format")

    @staticmethod
    def get_img_faces_dialog():
        """Get img path"""
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if not file_path:
            return

        image = fr.load_image_file(file_path)
        face_encodings = fr.face_encodings(image)
        for face_encoding in face_encodings:
            success, sid = get_id(face_encoding)
            if not success:
                continue
            now = datetime.now().strftime('%H:%M:%S')
            attendence[f"{sid}"] = now

        HandleBoard.writeData()

    @staticmethod
    def get_video_faces_dialog():
        """Get video path and process video for faces"""
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mov")])
        if not file_path:
            return

        video_capture = cv2.VideoCapture(file_path)
        while video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                break

            rgb_frame = frame[:, :, ::-1]
            face_encodings = fr.face_encodings(rgb_frame)
            for face_encoding in face_encodings:
                success, sid = get_id(face_encoding)
                if not success:
                    continue
                now = datetime.now().strftime('%H:%M:%S')
                attendence[f"{sid}"] = now

        video_capture.release()
        HandleBoard.writeData()

    @staticmethod
    def writeData():
        tree.delete(*tree.get_children())
        dt = date.today()
        with open(f'{dt}.csv', 'w', newline='') as csvfile:
            fieldnames = ['ID', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for k, v in get_attendence().items():
                writer.writerow({'ID': k, 'Time': v})
                tree.insert('', 'end', values=(k, v))

    @staticmethod
    def update_table():
        tree.delete(*tree.get_children())
        for k, v in get_attendence().items():
            tree.insert('', 'end', values=(k, v))

    @staticmethod
    def get_folder_encodes_dialog():
        """Get folder path and pass it to Encoder.store_encodes"""
        folder_path = filedialog.askdirectory()
        if not folder_path:
            return
        Encoder.store_encodes(folder_path)
        encodes = Encoder.get_encodes()
        messagebox.showinfo("Encodes Updated", f"Stored encodings from {folder_path}.\nTotal encodes: {len(encodes)}")

    @staticmethod
    def load_attendance_for_date():
        date_str = date_entry.get()
        HandleBoard.get_past(date_str)
        HandleBoard.show_attendance_window(date_str)

    @staticmethod
    def show_attendance_window(date_str):
        attendance_window = Toplevel(window)
        attendance_window.title(f"Attendance for {date_str}")
        attendance_window.geometry('400x300')

        attendance_tree = ttk.Treeview(attendance_window, columns=('ID', 'Time'), show='headings')
        attendance_tree.heading('ID', text='ID')
        attendance_tree.heading('Time', text='Time')
        attendance_tree.pack(fill=BOTH, expand=True)

        for k, v in get_attendence().items():
            attendance_tree.insert('', 'end', values=(k, v))

if __name__ == '__main__':
    HandleBoard.get_past(show_error=False)

    # GUI
    window = Tk()
    window.title("Face Recognition Attendance System")
    window.geometry('700x500')

    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), padding=10)
    style.configure('TLabel', font=('Helvetica', 14))
    style.configure('Treeview.Heading', font=('Helvetica', 12, 'bold'))

    # Upload button for image
    upload_button = ttk.Button(window, text="Choose Image", command=HandleBoard.get_img_faces_dialog)
    upload_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

    # Upload button for video
    video_button = ttk.Button(window, text="Choose Video", command=HandleBoard.get_video_faces_dialog)
    video_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

    # Upload button for folder
    folder_button = ttk.Button(window, text="Choose Folder", command=HandleBoard.get_folder_encodes_dialog)
    folder_button.grid(row=0, column=2, padx=10, pady=10, sticky='ew')

    # Date entry and button
    date_label = ttk.Label(window, text="Enter Date (YYYY-MM-DD):")
    date_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')

    date_entry = ttk.Entry(window)
    date_entry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

    load_date_button = ttk.Button(window, text="Load Attendance", command=HandleBoard.load_attendance_for_date)
    load_date_button.grid(row=1, column=2, padx=10, pady=10, sticky='ew')

    # Display table for detected users
    tree = ttk.Treeview(window, columns=('ID', 'Time'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Time', text='Time')
    tree.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

    # Add a scrollbar
    scrollbar = ttk.Scrollbar(window, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=2, column=3, sticky='ns')

    # Initialize table with existing data
    HandleBoard.update_table()

    window.grid_rowconfigure(2, weight=1)
    window.grid_columnconfigure(1, weight=1)

    window.mainloop()
    storage.save()
