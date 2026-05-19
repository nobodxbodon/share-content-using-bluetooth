import sys
import asyncio
import threading
import logging
from pathlib import Path

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
请求前缀 = "请求:"
回复前缀 = "回复:"

# NOTE: Some systems require different synchronization methods.
触发器: Union[asyncio.Event, threading.Event]
if sys.platform in ["darwin", "win32"]:
    触发器 = threading.Event()
else:
    触发器 = asyncio.Event()


async def 中(loop):
    触发器.clear()
    日志.info("Starting server...")
    # Instantiate the server
    # macOS BLE advertising data is small. A short name leaves room for the
    # 128-bit service UUID, so Windows clients can discover this server by UUID.
    服务器 = BlessServer(name=各识别码.设备名称, loop=loop)

    def 发送通知(characteristic: BlessGATTCharacteristic, 内容: str):
        characteristic.value = 内容.encode('utf-8')
        服务器.update_value(各识别码.服务识别码, 各识别码.特征识别码)

    def 判断路径(路径: str):
        return '存在' if Path(路径).exists() else '不存在'

    def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
        内容 = value.decode('utf-8').strip()
        日志.info(f"Received data: {内容}")

        if 内容.startswith(请求前缀):
            路径 = 内容.removeprefix(请求前缀).strip()
            回复 = 判断路径(路径)
            发送通知(characteristic, 回复前缀 + 回复)
            日志.info(f"Response sent: {回复}")
        elif 内容.startswith(回复前缀):
            日志.info(f"Received response: {内容.removeprefix(回复前缀)}")
        else:
            日志.warning(f"Unknown message: {内容}")

    async def 读取输入并发送请求(characteristic: BlessGATTCharacteristic):
        while True:
            路径 = await asyncio.to_thread(input, "请输入要让对端检查的路径（直接回车退出）：")
            路径 = 路径.strip()
            if not 路径:
                if 触发器.__module__ == "threading":
                    触发器.set()
                else:
                    触发器.set()
                break

            发送通知(characteristic, 请求前缀 + 路径)
            日志.info("Path request sent.")

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
    特征 = 服务器.get_characteristic(各识别码.特征识别码)
    asyncio.create_task(读取输入并发送请求(特征))

    if 触发器.__module__ == "threading":
        await asyncio.to_thread(触发器.wait)
    else:
        await 触发器.wait()

    await 服务器.stop()
    日志.info("Server stopped.")

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(中(loop))

except Exception as e:
    日志.error(f"An error occurred: {e}")
