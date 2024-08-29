import asyncio
import websockets
import random
import json
import serial

websocketURI = "ws://127.0.0.1:6789/"
#websocketURI = "ws://192.168.1.126:6789/"
#websocketURI = "ws://10.0.3.44:6789/"

ArduinoSerialPort = 'COM6'  # Replace with your port name (e.g., '/dev/ttyUSB0' for Linux)
ArduinoBaudRate = 115200

ArduinoEnabled = False
#####################################################################################
#########               ---------HOUSE VARIABLES--------                    #########
#####################################################################################


#####                     ------LIGHTS VARIABLES--------                        #####
light_rooms_entities = [
    "bedroom_lights",
    "kitchen_lights",
    "sitting_room_lights"
]
bedroom_lights_entities = [
    "bedroom-spots",
    "bedroom-pendant",
    "bedroom-accent",
    "bedroom-lamps"
]
kitchen_lights_entities = [
    
    "kitchen-spots",
    "kitchen-pendant", 
    "kitchen-accent",
    "kitchen-counter"
]
sitting_room_lights_entities = [
    "sitting-room-pendant", 
    "sitting-room-spots",
    "sitting-room-accent",
    "sitting-room-lamps"
]
lights_state = {
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
    "bedroom-lamps": True,
    "bedroom_lights": True,
    "kitchen_lights": True,
    "sitting_room_lights": True
}
lights_arduino_pins = {
    "kitchen-spots": 2,
    "kitchen-pendant": 13, 
    "kitchen-accent": 4,
    "kitchen-counter" : 5,
    "sitting-room-pendant": 6, 
    "sitting-room-spots": 7,
    "sitting-room-accent" : 22,
    "sitting-room-lamps": 23,
    "bedroom-pendant": 24, 
    "bedroom-spots": 25,
    "bedroom-accent" : 26,
    "bedroom-lamps": 27
}
#####                     ------ENERGY VARIABLES--------                        #####
energy_entities = [
    "solarstat",
    "windstat",
    "homestat",
    "gridstat",
    "gridcoststat"
]
energy_state = {
    "windstat" : "2.4kW",
    "solarstat" : "5.4kW",
    "homestat" : "3.4kW",
    "gridstat" : "1.4kW",
    "gridcoststat" : "$234"
}
#####                     ------BLIND VARIABLES--------                        #####
blind_command_entities = [
    "sitting-room-blind-command",
    "kitchen-blind-command",
    "skylight-blind-command"
]
blind_state_entities = [
    "sitting-room-blind-state",
    "kitchen-blind-state",
    "skylight-blind-state"
]
blind_states = {
    "sitting-room-blind-command":50,
    "sitting-room-blind-state":50,
    "kitchen-blind-command":50,
    "kitchen-blind-state":50,
    "skylight-blind-command":10,
    "skylight-blind-state":10
}
#####                     ------HEAT VARIABLES--------                        #####
heat_command_entities = [
    "sitting-room-blind-command",
    "kitchen-blind-command",
    "skylight-blind-command"
]
heat_state_entities = [
    "sitting-room-blind-state",
    "kitchen-blind-state",
    "skylight-blind-state"
]
heat_states = {
    "sitting-room-blind-command":30,
    "sitting-room-blind-state":30,
    "kitchen-blind-command":20,
    "kitchen-blind-state":20,
    "skylight-blind-command":18,
    "skylight-blind-state":18
}


#####                     ------OTHER ENTITIES--------                        #####
other_entities = [
    "thermostat",
    "alarm-system"
    ]
entities_state = {
    "bedroom-spots": True,
    "thermostat": True,  # in Celsius
    "alarm-system": False,
}




async def send_message(ws, message):
    await ws.send(message)
    print(f"Sent: {message}")

async def write_to_serial(arduino, message):
    # Write a message to the serial port
    if (ArduinoEnabled):
        arduino.write(message.encode('utf-8') + b'\n')
        print(f"Sent to serial: {message}")



###########################################################################
#####                     ------LIGHTS--------                        #####
###########################################################################

#####  ---receive websocket light commands and responding with updated light states---  #####
async def receive_light_update_messages(Arduino, ws, command):
    if command["num_server_entities"] == 1:
        entity = command["entities"][0]["entity"]
        state = command["entities"][0]["state"]
        lights_state[entity] = True if state else False
        command["state"] = lights_state[entity]
        command["num_entities"] = 1
        command["num_server_entities"] = 0
        message = json.dumps(command)
        await send_message(ws,message)
        await send_light_command_message(Arduino, entity, state)
    #print(entity, state,entities_state[entity])


#####  ---update room entities state by checking all lights in that room---   #####


async def update_room_group_status(ws):
    for r in range(len(light_rooms_entities)):
        room_list = globals().get(light_rooms_entities[r]+"_entities")
        lights_state[light_rooms_entities[r]] = False
        for i in range(len(room_list)):
            if (lights_state[room_list[i]] == True): 
                lights_state[light_rooms_entities[r]] = True 
                #draft_message = {"operation":"update","page":"lights","num_entities":1,"num_server_entities":0,"entities":[{"entity":room_list[i], "state":True}]}
                #print(draft_message)
                #message = json.dumps(draft_message)
                #await send_message(ws,message)
    #####     ------send light commands to arduino--------     #####
async def send_light_command_message(Aruduino, entity, state):
    entity_pin = lights_arduino_pins[entity]
    print("command to arduino: set " + entity + " to " + str(state) + " at pin " + str(entity_pin))
    message = {"msg":"REQ", "device_type":"light", "pin":entity_pin, "state":state}
    message = json.dumps(message)
    await write_to_serial(Aruduino, message)
    #connect to arduino and send command

"""
async def send_light_update_messages(ws, message):
    num_entities = message["num-sever-entities"]
    for i in range(num_entities):
        entity = message["entities"][i]["entity"]
        state = message["entities"][i]["entity"]
        if state != lights_state[entity]:
            lights_state[entity] = state
            draft_message = {"operation":"update","page":"lights","num_entities":1,"num_server_entities":0,"entities":[{"entity":entity, "state":state}]}
            await update_room_group_status(ws)
            await send_message(ws,draft_message)
            """


###########################################################################
#####                     ------BLINDS--------                        #####
###########################################################################


    #####     ------send states of sliders after reload--------     #####
async def send_blind_command_status(ws):
    
    draft_entities_list = []
    entities_list= globals().get("blind_command_entities")
    num_entities = len(entities_list)
    for i in range(num_entities):
        draft_entities_list.append({"entity":entities_list[i],"state":blind_states[entities_list[i]]})
    draft_message = {"operation":"state_status","page":"blinds","num_entities":num_entities,"num_server_entities":0,"entities":draft_entities_list}
    print(draft_message)
    message = json.dumps(draft_message)
    await ws.send(message)
    print(f"Sent: {message}")
    
async def send_blind_state_status(ws):
    draft_entities_list = []
    entities_list= globals().get("blind_state_entities")
    
    num_entities = len(entities_list)
    for i in range(num_entities):
        draft_entities_list.append({"entity":entities_list[i],"state":blind_states[entities_list[i]]})
    draft_message = {"operation":"state_status","page":"blinds","num_entities":num_entities,"num_server_entities":0,"entities":draft_entities_list}
    message = json.dumps(draft_message)
    await ws.send(message)
    print(f"Sent: {message}")

    #####     ------send commands to arduino--------     #####
async def send_blind_command_message(Aruduino, entity, value):
    print("command to arduino: set " + entity + " to " + str(value))
    message = {"msg":"REQ", "device_type":"blinds", "entity":"sitting-room-blind-command", "value":(value * 10)}
    message = json.dumps(message)
    blind_states[entity] = value
    await write_to_serial(Aruduino, message)
    #connect to arduino and send command


    #####     ------receive command messages from websocket--------     #####
async def receive_blind_command_message(Arduino, ws, command):
    entity = command["entities"][0]["entity"]
    value = command["entities"][0]["value"]
    blind_states[entity] =  value
    await send_blind_command_message(Arduino, entity, value)
    await send_blind_command_status(ws)
    
    #####     ------send single blind state update to websocket--------     #####
async def send_blind_state_message(ws, entity, value):
    draft_message = {"reload":0,"operation":"blind_update", "page":"blinds","num_entities":1,"num_server_entities":0,"entities":[{"entity":entity, "state":int(value/10)}]}
    message = json.dumps(draft_message)

    await ws.send(message)



#########################################################################
#####                     ------HEAT--------                        #####
#########################################################################

async def simulate_heating_change(entity, current_value, target_value):
    pass                                                                                        ###TODO
    #connect to arduino and send command
    
async def resdfceive_heat_command_message(ws,command):
    async for message in ws:
        command = json.load(message)
        if(command["operation"] == "client_update_heat"):
            entity = command["entities"][0]["entity"]
            target_value = command["entities"][0]["value"]
            current_value = heat_states["{entity}_state"]
            heat_states["{entity}_command"] = target_value
            await simulate_heating_change(entity, current_value, target_value)

async def sensdfd_blind_state_message(ws, entity, value):
    draft_message = {"reload":0,"operation":"blind_update", "page":"blinds","num_entities":1,"num_server_entities":0,"entities":[{"entity":entity, "value":value}]}
    message = json.dumps(draft_message)
    await ws.send(draft_message)

async def recsdfieve_blind_state_message(ws, message):
    num_entities = message["num_server_entities"]
    for i in range(num_entities):
        entity = message["entities"][0]["entity"]
        value = message["entities"][0]["value"]
        if blind_states[entity] != value:
            blind_states[entity] = value
            await send_blind_state_message(ws, entity, value)


##################################################################################
#####                     ------RELOADED PAGE--------                        #####
##################################################################################


async def send_state_status(ws,page):
    draft_entities_list = []
    await update_room_group_status(ws)
    entities_list= globals().get(page+"_entities")
    num_entities = len(entities_list)
    for i in range(num_entities):
        draft_entities_list.append({"entity":entities_list[i],"state":lights_state[entities_list[i]]})
    draft_message = {"operation":"state_status","page":page,"num_entities":num_entities,"num_server_entities":0,"entities":draft_entities_list}
    print(draft_message)
    message = json.dumps(draft_message)
    await ws.send(message)
    print(f"Sent: {message}")


#####                     ------TEmporary--------                        #####

async def receive_websocket_updates(Arduino, ws):
    async for message in ws:
        command = json.loads(message)
        if (command["operation"] == "reload"):
                page = command["page"]
                if page == "blinds":
                    await send_blind_state_status(ws)
                    await send_blind_command_status(ws)
                else:
                    await send_state_status(ws,page)

        elif (command["num_server_entities"] >= 1):
            print(f"Received: {message}")
            
            

            if (command["operation"] == "client_update_blinds"):
                await receive_blind_command_message(Arduino, ws, command)
            
            elif (command["operation"] == "client_update_heat"):
                await receive_heat_command_message(ws, command)

            elif (command["operation"] == "client_update_lights"):
                await receive_light_update_messages(Arduino, ws, command)

            """
            else:
                num_entities = command["num_server_entities"]
                if (num_entities == 1):
                    entity = command["entities"][0]["entity"]
                    state = command["entities"][0]["state"]
                    entities_state[entity] = True if state else False
                    command["state"] = entities_state[entity]
                    command["num_entities"] = 1
                    command["num_server_entities"] = 0
                    message = json.dumps(command)
                    await send_message(ws,message)
                    print(entity, state,entities_state[entity])
                    """

#####                     ------ENERGY--------                        #####
async def query_energy():
    print("send query request to arduino")
    #TODO 

async def send_energy_update(ws, entity, value):
    draft_message = {"reload":0,"operation":"energy_update", "page":"energy","num_entities":1,"num_server_entities":0,"entities":[{"entity":entity, "value":value}]}
    await ws.send(draft_message)


async def recieve_energy_update(ws, message):
    num_entities = message["num_server_entities"]
    for i in range(num_entities):
        entity = message["entities"][0]["entity"]
        value = message["entieties"][0]["value"]
        if energy_state[entity] != value:
            energy_state[entity] = value
            await send_energy_update(ws,entity,value)



async def read_from_serial(serial_reader, ws):
    if (ArduinoEnabled):
        while True:
            # Read from the serial port
            if serial_reader.in_waiting:
                data = serial_reader.readline().decode('utf-8').strip()        
                #print(f"Serial received: {data}")
                message = json.loads(data)
                #print(message)
                if (message['msg'] == 'state'):
                    await send_blind_state_message(ws, "sitting-room-blind-state", message["value"])
            await asyncio.sleep(0.1)


async def recieve_serial (ws):
    pass
        












#####                     ------MAIN--------                        #####


async def main():

    try:
        if (ArduinoEnabled):
            ArduinoSerial = serial.Serial(ArduinoSerialPort, ArduinoBaudRate, timeout=1)
        else:
            ArduinoSerial = "not enabled"
            print("Arduino not enabled")
        try:
            async with websockets.connect(websocketURI) as ws:
                print("Connected to WebSocket server")
                await asyncio.gather(

                    receive_websocket_updates(ArduinoSerial, ws),
                    read_from_serial(ArduinoSerial, ws)
                
                )
        finally:
            print("failed to connect to Websocket")
            ArduinoSerial.close()

    except:
        print("Failed to open Serial Port")
    
    


if __name__ == "__main__":
    asyncio.run(main())