import face_recognition
import numpy as np
from PIL import Image

def encode_face(image_path):
    img = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(img)
    return encodings[0] if encodings else None

def compare_faces(encoding1, encoding2, tolerance=0.6):
    if encoding1 is None or encoding2 is None:
        return False
    distance = face_recognition.face_distance([encoding1], encoding2)[0]
    return distance < tolerance

def extract_face_from_id(id_image_path):
    img = face_recognition.load_image_file(id_image_path)
    face_locations = face_recognition.face_locations(img)
    if not face_locations:
        return None
    encodings = face_recognition.face_encodings(img, face_locations)
    return encodings[0] if encodings else None
