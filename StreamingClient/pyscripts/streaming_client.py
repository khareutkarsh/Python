"""
This is the closs which behaves as a streaming client to send and receive the account and transactions
"""
import asyncio
import logging
import sys


class StreamingClient:

    # initializing the class
    def __init__(self, logging, ip, port,header_size):
        self.logging = logging
        self.ip = ip
        self.port = port
        self.header_size = header_size

    # Method to send and receive from the server
    async def send_and_receive(self, message):
        try:
            reader, writer = await asyncio.open_connection(self.ip, self.port)
            self.logging.info(f'Send: {message!r}')
            data = message.encode()
            data_header = f"{len(message) :< {self.header_size}}".encode()
            writer.write(data_header + data)
            await writer.drain()

            data_header = await reader.read(self.header_size)
            message_header = data_header.decode()
            message_length = int(message_header)
            data = await reader.read(message_length)
            message = data.decode()

            self.logging.info(f'Received: {message!r}')
        except Exception as e:
            self.logging.error(e)
        finally:
            writer.close()
            await writer.wait_closed()

    # Method to take command line input from the user and call send_receive method to communicate with server
    async def send_streams(self):
        try:
            while True:
                message = input("enter the message:")
                await self.send_and_receive(message)

        except Exception as e:
            self.logging.error(e)


# Main to execute the command line client
if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(module)s[%(filename)s:%(lineno)d] %(message)s',
        datefmt='%y/%d/%m %H:%M:%S',
        level=logging.INFO)
    if len(sys.argv) >= 2:
        client = StreamingClient(logging, sys.argv[1],sys.argv[2],10)
        asyncio.run(client.send_streams())
    else:
        print("Please provide IP  and PORT(as given for server) as arguments to run the client")
