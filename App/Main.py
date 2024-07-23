from flask import Flask, render_template, request, jsonify, Response
from camera import VideoCamera


app = Flask(__name__)

camera = VideoCamera()

devices = {
    "bedroom-spots": True,
    "thermostat": 22,  # in Celsius
    "alarm-system": False
}

lights = {
    "kitchen-spots": True,
    "kitchen-pendant": True, 
    "kitchen-accent": True,
    "kitchen-counter" : True,
    "sitting-room-pendant": True, 
    "sitting-room-spots": True,
    "sitting-room-accent" : True,
    "sitting-room-lamps": True,
    "bedroom-pendant": True, 
    "bedroom-spots": True,
    "bedroom-accent" : True,
    "bedroom-lamps": True
}






@app.route('/index')
def index():
    return render_template('index.html', devices=devices)



@app.route('/')
def home():
    return render_template('home.html', devices=devices)

                    #######Lights

@app.route('/lights')
def lights_menu():
    return render_template('lights/lights.html', lights=lights)
@app.route('/kitchen-lights')
def kitchen_lights():
    return render_template('lights/kitchen-lights.html', lights=lights)


@app.route('/sitting-room-lights')
def sitting_room_lights():
    return render_template('lights/sitting-room-lights.html', lights=lights)
@app.route('/bedroom-lights')
def bedroom_lights():
    return render_template('lights/bedroom-lights.html', lights=lights)


                    ##### Security


@app.route('/security')
def security():
    return render_template('security.html', devices=devices)


@app.route('/security/video_feed')
def video_feed():
    return Response(camera.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')





                    ####### Blinds
@app.route('/blinds')
def blinds():
    return render_template('blinds.html', devices=devices)

                    ###### watch
@app.route('/watch')
def watch():
    return render_template('watch.html', devices=devices)

                 ####### heat
@app.route('/heat')
def heat():
    return render_template('heat.html', devices=devices)

                    ###### energy
@app.route('/energy')
def energy():
    return render_template('energy.html', devices=devices)



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)