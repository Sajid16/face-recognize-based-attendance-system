from __future__ import print_function
import face_recognition
import os
import glob
import time
import cx_Oracle
import cv2
import numpy as np
from datetime import datetime
from math import hypot
import dlib


def facerecognitionReg(username, officecode):
    def scan_known_people(known_people_folder):
        known_names = []
        known_face_encodings = []
        for file in known_people_folder:
            basename = os.path.splitext(os.path.basename(file))[0]
            img = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(img)
            known_names.append(basename)
            known_face_encodings.append(encodings[0])
        return known_names, known_face_encodings

    # Multiple Image read  from Folder
    path = os.path.join("saved_images/" + officecode + "/", '*g')

    # path = os.path.join("saved_images/", '*g')
    known_people_folder = glob.glob(path)

    known_face_names, known_face_encodings = scan_known_people(known_people_folder)

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    Time = time.strftime("%Y%m%d-%H%M%S")
    flag = 0  # Identification Value

    frame_image = face_recognition.load_image_file('./verify_images/' + officecode + "/" + username)

    # ..................Face Recognition Start.............................
    flag = 0
    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame_image)
    face_encodings = face_recognition.face_encodings(frame_image, face_locations)

    face_names = []
    count = 0
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55)
        name = "Unknown"
        count += 1
        # If a match was found in known_face_encodings, just use the first one.
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            flag = 1
        face_names.append(name)
    print("face REcog ", flag)
    return flag


