import cv2


def blur(image, ksize=(150, 150)):
    blurred = cv2.blur(image, ksize)
    return blurred
