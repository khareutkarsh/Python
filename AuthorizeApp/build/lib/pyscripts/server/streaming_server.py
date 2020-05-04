"""
This is the server class where the streaming server is started to listen on a port and handle the requests sent by a streaming client
"""
import asyncio
from json import JSONDecodeError
from pyscripts.constants.app_constants import *
from pyscripts.business_rules.manage_account import ManageAccount
from pyscripts.util import logging_util, message_utils
from pyscripts.business_rules.authorize_transaction import AuthorizeTransaction


class StreamingServer:

    # initializing the class members
    def __init__(self):
        self.logging = logging_util.get_logger()
        self.account_svc = ManageAccount()
        self.authorize_svc = AuthorizeTransaction()

    # method to receive the requests sent by streaming client and send a response after processing them
    async def handle_requests(self, reader, writer):
        try:
            data_header = await reader.read(HEADERSIZE)
            message_header = data_header.decode()
            message_length = int(message_header)
            data = await reader.read(message_length)
            message = data.decode()
        except JSONDecodeError as e:
            self.logging.error(e)
            exception_response = '{"error": "Expecting a value in the received message"}'
            exception_response_data = exception_response.encode()
            exception_response_header = f"{len(exception_response) :< {HEADERSIZE}}".encode()
            writer.write(exception_response_header + exception_response_data)
            await writer.drain()
        else:
            addr = writer.get_extra_info("peername")
            self.logging.info(f"Received {message!r} from {addr!r}")
            response = ""
            try:
                request_type = message_utils.get_request_type(message, self.logging)
                if request_type == "ACCOUNT":
                    response = self.account_svc.create_account(message, self.logging)
                elif request_type == "TRANSACTION":
                    response = self.authorize_svc.process_transaction(message, self.account_svc, self.logging)
            except Exception as e:
                self.logging.error(e)
                exception_response = '{"error": "Error in processing the received message"}'
                exception_response_data = exception_response.encode()
                exception_response_header = f"{len(exception_response) :< {HEADERSIZE}}".encode()
                writer.write(exception_response_header + exception_response_data)
                await writer.drain()
            else:
                self.logging.info(f"Send: {response !r}")
                response_data = response.encode()
                response_header = f"{len(response) :< {HEADERSIZE}}".encode()
                writer.write(response_header + response_data)
                await writer.drain()

        finally:
            writer.close()

    # method to start the server
    async def start(self, host_ip, host_port):
        try:
            if host_ip and host_port:
                server = await asyncio.start_server(self.handle_requests, host_ip, host_port)
                addr = server.sockets[0].getsockname()
                self.logging.info(f'Serving on {addr}')

                async with server:
                    await server.serve_forever()
            else:
                raise ValueError("one of port and socket_path must be provided.")

        except Exception as e:
            self.logging.error(e)
        finally:
            server.close()
