import sys
import asyncio
import threading

from typing import Any, Union

from bless import BlessServer
from bless import BlessGATTCharacteristic
from bless import GATTCharacteristicProperties
from bless import GATTAttributePermissions

from the_uuids import UUID as UUIDs

uuids = UUIDs()

# NOTE: Some systems require different synchronization methods.
trigger: Union[asyncio.Event, threading.Event]
if sys.platform in ["darwin", "win32"]:
    trigger = threading.Event()
else:
    trigger = asyncio.Event()


async def run(loop):
    trigger.clear()
    # Instantiate the server
    my_service_name = "Test Service"
    server = BlessServer(name=my_service_name, loop=loop)

    def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
        print(value.decode('utf-8'))
        characteristic.value = '我吃了'.encode('utf-8')
        server.update_value(uuids.service_uuid, uuids.characteristic_uuid)

    server.write_request_func = write_request

    # Add Service
    await server.add_new_service(uuids.service_uuid)

    # Add a Characteristic to the service
    char_flags = (
            GATTCharacteristicProperties.write
            | GATTCharacteristicProperties.notify
    )
    permissions = GATTAttributePermissions.readable | GATTAttributePermissions.writeable
    await server.add_new_characteristic(
        uuids.service_uuid, uuids.characteristic_uuid, char_flags, None, permissions
    )

    await server.start()
    if trigger.__module__ == "threading":
        # noinspection PyAsyncCall
        trigger.wait()
    else:
        await trigger.wait()

    await server.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
