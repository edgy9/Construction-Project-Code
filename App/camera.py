import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        if not (self.video.isOpened()):
            print("Could not open video device")

    def __del__(self):
        self.video.release()        

    def get_frame(self):
        ret, frame = self.video.read()

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()