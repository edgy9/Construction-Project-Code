from flask import Flask, render_template, request, jsonify,Response
from camera import VideoCamera
import cv2


app = Flask(__name__)


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



video_stream = VideoCamera()



@app.route('/light-state-status')
def light_state_status():
    return jsonify(lights)


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

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/security/video_feed')
def video_feed():
     return Response(gen(video_stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')        




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

@app.route('/toggle-light/<light>', methods=['POST'])
def toggle_light(light):
    if light in lights:
        lights[light] = not lights[light] if isinstance(lights[light], bool) else lights[light]
        #print("changed state")
        return jsonify(success=True, state=lights[light])
    return jsonify(success=False)




@app.route('/toggle/<device>', methods=['POST'])
def toggle_device(device):
    if device in devices:
        devices[device] = not devices[device] if isinstance(devices[device], bool) else devices[device]
        #print("changed state")
        return jsonify(success=True, state=devices[device])
    return jsonify(success=False)

if __name__ == '__main__':
    app.run(debug=True)