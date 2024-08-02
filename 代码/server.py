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

日志 = logging.getLogger(__name__)

各识别码 = 唯一识别码()

# NOTE: Some systems require different synchronization methods.
触发器: Union[asyncio.Event, threading.Event]
if sys.platform in ["darwin", "win32"]:
    触发器 = threading.Event()
else:
    触发器 = asyncio.Event()


async def run(loop):
    触发器.clear()
    日志.info("Starting server...")
    # Instantiate the server
    my_service_name = "Test Service"
    服务器 = BlessServer(name=my_service_name, loop=loop)

    def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
        日志.info(f"Received data: {value.decode('utf-8')}")
        characteristic.value = '我吃了'.encode('utf-8')
        服务器.update_value(各识别码.服务识别码, 各识别码.特征识别码)

    服务器.write_request_func = write_request

    # Add Service
    await 服务器.add_new_service(各识别码.服务识别码)
    日志.info("Service added.")

    # Add a Characteristic to the service
    char_flags = (
            GATTCharacteristicProperties.write
            | GATTCharacteristicProperties.notify
    )
    permissions = GATTAttributePermissions.readable | GATTAttributePermissions.writeable
    await 服务器.add_new_characteristic(
        各识别码.服务识别码, 各识别码.特征识别码, char_flags, None, permissions
    )
    日志.info("Characteristic added.")

    await 服务器.start()
    日志.info("Server started.")

    if 触发器.__module__ == "threading":
        # noinspection PyAsyncCall
        触发器.wait()
    else:
        await 触发器.wait()

    await 服务器.stop()
    日志.info("Server stopped.")

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))

except Exception as e:
    日志.error(f"An error occurred: {e}")