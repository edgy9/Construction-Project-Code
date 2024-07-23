from flask import Flask, render_template, Response
from camera import VideoCamera


app = Flask(__name__)

camera = VideoCamera()




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(camera.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')





   
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

