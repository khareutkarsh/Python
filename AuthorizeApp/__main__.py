"""This the main entry point of the streaming server , which starts the server to listen on a host and port for the
requests. """

from pyscripts.constants.app_constants import *
import asyncio
from pyscripts.server.streaming_server import StreamingServer

# the main method to start the server
if __name__ == "__main__":

    server = StreamingServer()
    asyncio.run(server.start(IP, PORT))
