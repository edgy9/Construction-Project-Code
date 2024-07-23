import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

        if not (self.video.isOpened()):
            print("Could not open video device")

    def __del__(self):
        self.video.release()        

    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            raise RuntimeError("Failed to capture image")
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            raise RuntimeError("Failed to encode image")
        return buffer.tobytes()
    def generate_frames(self):
        while True:
            frame = self.get_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')