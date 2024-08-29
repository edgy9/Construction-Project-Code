from flask import Flask, render_template, request, jsonify, Response
from camera import VideoCamera

URIdata = {"URI":"ws://127.0.0.1:6789/"}
#URIdata = {"URI":"ws://192.168.1.126:6789/"}
#URIdata = {"URI":"ws://10.0.3.44:6789/"}

app = Flask(__name__)

camera = VideoCamera()


@app.route('/index')
def index():
    return render_template('index.html')



@app.route('/')
def home():
    return render_template('home.html')

                    #######Lights

@app.route('/lights')
def lights_menu():
    return render_template('lights/lights.html',URIdata=URIdata)

@app.route('/kitchen-lights')
def kitchen_lights():
    return render_template('lights/kitchen-lights.html', URIdata=URIdata)

@app.route('/sitting-room-lights')
def sitting_room_lights():
    return render_template('lights/sitting-room-lights.html', URIdata=URIdata)

@app.route('/bedroom-lights')
def bedroom_lights():
    return render_template('lights/bedroom-lights.html', URIdata=URIdata)


                    ##### Security


@app.route('/security')
def security():
    return render_template('security.html', URIdata=URIdata)


@app.route('/security/video_feed')
def video_feed():
    return Response(camera.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


                    ####### Blinds
@app.route('/blinds')
def blinds():
    return render_template('blinds.html', URIdata=URIdata)

                    ###### watch
@app.route('/watch')
def watch():
    return render_template('watch.html', URIdata=URIdata)

                 ####### heat
@app.route('/heat')
def heat():
    return render_template('heat.html', URIdata=URIdata)

                    ###### energy
@app.route('/energy')
def energy():
    return render_template('energy.html', URIdata=URIdata)



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)