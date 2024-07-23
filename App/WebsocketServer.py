import asyncio
import websockets

connected_clients = set()

async def handle_client(websocket, path):
  # Register the new client
  connected_clients.add(websocket)
  #await websocket.send('{"initialize":"True"}')
  #print("new client")
  try:
    async for message in websocket:
      await asyncio.wait([asyncio.create_task(client.send(message)) for client in connected_clients])
  finally:
    # Unregister the client
    connected_clients.remove(websocket)

async def main():
    server = await websockets.serve(handle_client, "192.168.1.130", 6789)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())