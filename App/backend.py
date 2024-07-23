import asyncio
import websockets
import random
import json
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
energy_entities = [
    "solarstat",
    "windstat",
    "homestat",
    "gridstat",
    "gridcoststat"
]
other_entities = [
    "thermostat",
    "alarm-system"
    ]


entities_state = {
    "bedroom-spots": True,
    "thermostat": True,  # in Celsius
    "alarm-system": False,
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
    "bedroom_lights" : True,
    "sitting_room_lights" : True,
    "kitchen_lights" : False,
    "windstat" : "2.4kW",
    "solarstat" : "5.4kW",
    "homestat" : "3.4kW",
    "gridstat" : "1.4kW",
    "gridcoststat" : "$234",
}

def update_room_status():
    for r in range(len(light_rooms_entities)):
        room_list = globals().get(light_rooms_entities[r]+"_entities")
        entities_state[light_rooms_entities[r]] = False
        for i in range(len(room_list)):
            if (entities_state[room_list[i]] == True): 
                entities_state[light_rooms_entities[r]] = True 


async def check_digital_output():
    await asyncio.sleep(20)  # Simulate a delay in state checking
    return random.choice([True, False])
async def check_power():  # Simulate a delay in state checking
    await asyncio.sleep(2)
    return round(random.random(), 3)

async def send_message(ws, message):
    await ws.send(message)
    print(f"Sent: {message}")

async def send_state_status(ws,page):
    draft_entities = []
    update_room_status()
    entities = globals().get(page+"_entities")
    num_entities = len(entities)
    for i in range(num_entities):
        draft_entities.append({"entity":entities[i],"state":entities_state[entities[i]]})
    draft_message = {"reload":0,"page":page,"num_entities":num_entities,"num_server_entities":0,"entities":draft_entities}
    message = json.dumps(draft_message)
    await ws.send(message)
    print(f"Sent: {message}")

async def receive_updates(ws):
    async for message in ws:
        print(f"Received: {message}")
        command = json.loads(message)
        if (command["reload"]): 
            page = command["page"]
            await send_state_status(ws,page)
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


async def digital_output_monitor(ws):
    last_state = None
    while True:
        await asyncio.sleep(10)
        entities_state["solarstat"] = await check_power()
        entities_state["windstat"] = await check_power()
        entities_state["homestat"] = await check_power()
        entities_state["gridstat"] = await check_power()
        await send_state_status(ws,"energy")
            

async def power_monitor(ws):
    while True:
        current_state = await check_digital_output()
        if current_state != last_state:
            #await send_message(ws, f"Digital output state changed to {current_state}")
            last_state = current_state

async def main():
    uri = "ws://192.168.1.130:6789"  
    async with websockets.connect(uri) as ws:
        receive_task = asyncio.create_task(receive_updates(ws))
        monitor_task = asyncio.create_task(digital_output_monitor(ws))
        await asyncio.gather(receive_task, monitor_task)

if __name__ == "__main__":
    asyncio.run(main())