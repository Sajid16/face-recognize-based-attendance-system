import cv2


def facedetectionReg(image, officecode):
    # multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
    faceCascade = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')

    test_image = cv2.imread('verify_images/' + officecode + "/" + image)

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
        flag = len(faces)
    print("face detect: ", flag)
    return flag
