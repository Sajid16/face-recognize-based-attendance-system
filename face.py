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

##############################  connecting database ##############################

dsn_tns = cx_Oracle.makedsn('10.11.201.51', '1521', 'APEXTEST')
conn = cx_Oracle.connect(user='PATTNDB', password='pattndb', dsn=dsn_tns)


##################################################################################


################################# required functions #############################
def scan_known_people(known_people_folder):
    branch_code = ''
    known_names = []
    known_face_encodings = []
    for file in known_people_folder:
        basename = os.path.splitext(os.path.basename(file))[0]
        img = face_recognition.load_image_file(file)
        encodings = face_recognition.face_encodings(img)
        known_names.append(basename)
        known_face_encodings.append(encodings[0])
    return known_names, known_face_encodings


def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def get_blinking_ratio(frame_image, eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line = cv2.line(frame_image, left_point, right_point, (0, 255, 0), 2)
    ver_line = cv2.line(frame_image, center_top, center_bottom, (0, 255, 0), 2)

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio


def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


###############################################################################################################


############################## detector and predictor for blink ###############################################

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


##########################################################################################################


#################################### main recognition function starts ##########################################

def facerecognitionFunction(username, branch_code, ip, lat, lon, s_id):
    p = conn.cursor()
    stmnt = "select PYHDRCDE,PYSOFCDE from VW_PYCODMAS where PYCODDES = '" + branch_code + "'"
    p.execute(stmnt)
    office = ''
    for row in p:
        office = row[0] + row[1]
    print('office value: ' + office)
    # Multiple Image read  from Folder
    path = os.path.join("saved_images/" + office + "/", '*g')
    # path = os.path.join("saved_images/", '*g')
    known_people_folder = glob.glob(path)

    # face encoding
    known_face_names, known_face_encodings = scan_known_people(known_people_folder)

    ###################################### Initialize some variables ################################

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    Time = time.strftime("%Y%m%d-%H%M%S")
    status_flag = 0
    flag = 0
    blink = 0
    empcde = 0
    approve_status = ''
    blink_condition_true = 0
    blink_condition_false = 0

    ###################################### Initialize some variables ################################

    for i in range(0, 15):
        username = str(i) + '.jpeg'
        frame_image = face_recognition.load_image_file('./check_images/' + s_id + '/' + username)

        ####### flag for recognition for the first time #####################
        if flag == 0:

            # ..................Face Recognition Start.............................

            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(frame_image)
            try:
                if len(face_locations) < 1:
                    print("Found {0} faces!".format(len(face_locations)))
            except:
                print("Error flash message")

            face_encodings = face_recognition.face_encodings(frame_image, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.55)
                name = "Unknown"
                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                    flag = 1
                    break
            face_names.append(name)
            print("Face Identified Value: " + str(flag) + ' name ' + name)
            if name == "Unknown":
                return flag, status_flag, empcde, blink


        ############## recognition complete #############
        else:
            # ..................Face Recognition End.............................

            # ..........................EYE BLINKING Code Start..........................

            # ....................Device Detection Start...............
            # image_file = './check_images/' + username  # testing image path
            # config_file = 'device/yolo.cfg'  # cfg file path
            # weights_file = 'device/yolov3.weights'  # weights file path
            # classes_file = 'device/classes.txt'  # containing class names file path
            # device = 0
            #
            # image = cv2.imread(image_file)
            #
            # scale = 0.00392
            #
            # with open(classes_file, 'r') as f:
            #     classes = [line.strip() for line in f.readlines()]
            #
            # COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
            # net = cv2.dnn.readNet(weights_file, config_file)
            # blob = cv2.dnn.blobFromImage(image, scale, (640, 480), (0, 0, 0), True, crop=False)
            # net.setInput(blob)
            #
            # outs = net.forward(get_output_layers(net))
            # for out in outs:
            #     for detection in out:
            #         scores = detection[5:]
            #         class_id = np.argmax(scores)
            #         confidence = scores[class_id]
            #         if confidence > 0.5:
            #             label = str(classes[class_id])
            #             if label == 'cell phone':
            #                 device = 1
            #         else:
            #             pass
            #             # print("value of device: ", device)
            # # print(device)
            # # ....................Device Detection End...............

            # ..........................EYE BLINKING Code End..........................

            # ...................Eye Blinking Code Start.........................
            gray = cv2.cvtColor(frame_image, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)
            for face in faces:
                landmarks = predictor(gray, face)
                left_eye_ratio = get_blinking_ratio(frame_image, [36, 37, 38, 39, 40, 41], landmarks)
                right_eye_ratio = get_blinking_ratio(frame_image, [42, 43, 44, 45, 46, 47], landmarks)
                blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

                if blinking_ratio > 4.5:
                    print("blinking")
                    blink += 1

            # ...................Eye Blinking Code End.........................

            if blink > 1:
                comp_eid = name.split('_')
                compcde = comp_eid[0]
                empcde = comp_eid[1]
                log_time = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                log_time2 = datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                create_by = 'AUTO'

                check_approval = conn.cursor()
                stmnt = "select APPROVAL_FLG from REGISTER where EMPCDE = '" + empcde + "' and COMPCDE = '" + compcde + "'"
                check_approval.execute(stmnt)

                for row in check_approval:
                    approve_status = row[0]
                    print("value of approve_status: ", approve_status)

                # if approve_status == 'Y' and device == 0 and blink == 1:
                # if approve_status == 'Y' and blink == 0:
                if approve_status == 'Y':
                    c = conn.cursor()
                    stmnt = "insert into ATTN_LOG (COMPCDE, EMPCDE, IP_ADDRESS, LOG_TIME, CREATEBY, CREATEDT, LATTITUDE, LONGITUDE) " \
                            "values('{0}','{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')"
                    stmnt = stmnt.format(compcde, empcde, str(ip), log_time, create_by, log_time2, lat, lon)
                    c.execute(stmnt)
                    conn.commit()
                    status_flag = 1
                    return flag, empcde, status_flag, blink

                else:
                    status_flag = 0
                    return flag, empcde, status_flag, blink
        # else:
        # empcde = 0

    # return flag, empcde, status_flag, device, blink
    return flag, empcde, status_flag, blink
    # return flag, empcde, status_flag, device
