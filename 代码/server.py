import sys
import asyncio
import threading
import logging

from typing import Any, Union

from bless import BlessServer
from bless import BlessGATTCharacteristic
from bless import GATTCharacteristicProperties
from bless import GATTAttributePermissions

from the_uuids import 唯一识别码

# Configure logging
logging.basicConfig(
    level = logging.DEBUG,
    datefmt='%H:%M:%S',
    format = '%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("debug.log"),logging.StreamHandler()]
)

logger = logging.getLogger(__name__)

各识别码 = 唯一识别码()

# NOTE: Some systems require different synchronization methods.
trigger: Union[asyncio.Event, threading.Event]
if sys.platform in ["darwin", "win32"]:
    trigger = threading.Event()
else:
    trigger = asyncio.Event()


async def run(loop):
    trigger.clear()
    logger.info("Starting server...")
    # Instantiate the server
    my_service_name = "Test Service"
    server = BlessServer(name=my_service_name, loop=loop)

    def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
        logger.info(f"Received data: {value.decode('utf-8')}")
        characteristic.value = '我吃了'.encode('utf-8')
        server.update_value(各识别码.服务识别码, 各识别码.特征识别码)

    server.write_request_func = write_request

    # Add Service
    await server.add_new_service(各识别码.服务识别码)
    logger.info("Service added.")

    # Add a Characteristic to the service
    char_flags = (
            GATTCharacteristicProperties.write
            | GATTCharacteristicProperties.notify
    )
    permissions = GATTAttributePermissions.readable | GATTAttributePermissions.writeable
    await server.add_new_characteristic(
        各识别码.服务识别码, 各识别码.特征识别码, char_flags, None, permissions
    )
    logger.info("Characteristic added.")

    await server.start()
    logger.info("Server started.")

    if trigger.__module__ == "threading":
        # noinspection PyAsyncCall
        trigger.wait()
    else:
        await trigger.wait()

    await server.stop()
    logger.info("Server stopped.")

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))

except Exception as e:
    logger.error(f"An error occurred: {e}")