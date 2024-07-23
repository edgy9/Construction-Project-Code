
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)



# Simulated state of devices
devices = {
    "lights": False,
    "thermostat": 22,  # in Celsius
    "security_system": False
}

@app.route('/')
def index():
    return render_template('test.html', devices=devices)

@app.route('/toggle/<device>', methods=['POST'])
def toggle_device(device):
    if device in devices:
        devices[device] = not devices[device] if isinstance(devices[device], bool) else devices[device]
        app.logger.warning('light Toggled')
        app.logger.warning(devices[device])
        return jsonify(success=True, state=devices[device])
    return jsonify(success=False)

@app.route('/set_thermostat', methods=['POST'])
def set_thermostat():
    temperature = request.form.get('temperature')
    try:
        devices['thermostat'] = int(temperature)
        return jsonify(success=True, temperature=devices['thermostat'])
    except ValueError:
        return jsonify(success=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0')