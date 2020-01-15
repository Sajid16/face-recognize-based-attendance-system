'''
Haar Cascade Face detection with OpenCV
    Based on tutorial by pythonprogramming.net
    Visit original post: https://pythonprogramming.net/haar-cascade-face-eye-detection-python-opencv-tutorial/
Adapted by Marcelo Rovai - MJRoBot.org @ 7Feb2018
'''

import cv2


def facedetection(image):
    # multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

    test_image = cv2.imread('check_images/' + image)
    # test_image = cv2.imread('saved_images/images.jpg')

    gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,

        scaleFactor=1.2,
        minNeighbors=5
        ,
        minSize=(20, 20)
    )

    # print(type(faces))
    # print(len(faces))
    if len(faces) == 0:
        flag = 0
    else:
        flag = 1
    print(flag)
    return flag


# facedetection()

# for (x, y, w, h) in faces:
#     cv2.rectangle(test_image, (x, y), (x + w, y + h), (255, 0, 0), 2)
#     roi_gray = gray[y:y + h, x:x + w]
#     roi_color = test_image[y:y + h, x:x + w]
#
# cv2.imshow('video', test_image)
# k = cv2.waitKey(3000) & 0xff


