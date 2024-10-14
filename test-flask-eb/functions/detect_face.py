import cv2 as cv

def verify_human_face(image_path):
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    image = cv.imread(image_path)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) > 0:
        print("Human face(s) detected in the uploaded image.")
        return True
    else:
        print("No human faces detected in the uploaded image.")
        return False