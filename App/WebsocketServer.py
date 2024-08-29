import asyncio
import websockets

connected_clients = set()

URI = "127.0.0.1"
#URI = "192.168.1.126"
#URI = "10.0.3.44"



async def handle_client(websocket, path):
  connected_clients.add(websocket)
  #await websocket.send('{"initialize":"True"}')
  #print("new client")
  try:
    async for message in websocket:
      await asyncio.wait([asyncio.create_task(client.send(message)) for client in connected_clients])
  finally:
    connected_clients.remove(websocket)

async def main():
    server = await websockets.serve(handle_client, URI, 6789)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())