import asyncio
import json

from td_connect import TDAuth


async def main():
    
    auth = TDAuth.from_gcs_env()

    request = {
        "service": "LEVELONE_FUTURES",
        "command": "SUBS",
        "parameters": {
            "keys": "/ES",
            # Subscribe to Bid Price, Ask Price, Last Price, Bid Size.
            "fields": "0,1,2,3,4"
        }
    }
    # get a logged in and authenticated websocket connection.
    conn = await auth.get_stream_websocket()
    # connect to stream
    request = auth.authenticate_stream_requests(request)
    await conn.send(request)
    # receive stream data forever.
    while True:
        message = await conn.recv()
        message_decoded = json.loads(message)
        print(message_decoded)
        
        
if __name__=='__main__':
    asyncio.run(main())
