"""
This file is to execute the integration test by reading a series of input from a file and validating the response received from the server with the expected result
"""
import asyncio
import os,sys,logging

HEADERSIZE = 10
IP = "127.0.0.1"
PORT = "2222"
TEST_RESOURCES_DIR = "resources"
ACCOUNT_CREATION_FILE = "integration_testdata.txt"
logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(module)s[%(filename)s:%(lineno)d] %(message)s',
    datefmt='%y/%d/%m %H:%M:%S',
    level=logging.INFO)


async def test_streamapp(message):
    try:
        reader, writer = await asyncio.open_connection(IP, PORT)
        data = message.encode()
        data_header = f"{len(message) :< {HEADERSIZE}}".encode()
        writer.write(data_header + data)
        await writer.drain()

        data_header = await reader.read(HEADERSIZE)
        message_header = data_header.decode()
        message_length = int(message_header)
        data = await reader.read(message_length)
        response_message = data.decode()
        writer.close()
        await writer.wait_closed()
        writer.close()
        await writer.wait_closed()
        return response_message

    except Exception as e:
        logging.error(e)


async def initiate_integration_test():

    dir_name = os.path.dirname(__file__)
    test_file = dir_name+'/'+ACCOUNT_CREATION_FILE
    with open(test_file, 'r') as f:
        for line in f:
            input_expected_arr = line.split("|")
            response_message = await test_streamapp(input_expected_arr[0])
            if response_message == input_expected_arr[1].strip():
                logging.info(f"input :{input_expected_arr[0]} expected : {input_expected_arr[1].strip()} test result:PASS")
            else:
                logging.info(f"input :{input_expected_arr[0]} expected : {input_expected_arr[1].strip()} test result:FAIL")
                logging.info("Test Failed due to failure of above test step")
                sys.exit()


if __name__ == "__main__":
    asyncio.run(initiate_integration_test())
