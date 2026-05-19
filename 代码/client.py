import asyncio
import logging
from pathlib import Path
from bleak import BleakScanner, BleakClient, BLEDevice, AdvertisementData
from the_uuids import 唯一识别码

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    datefmt='%H:%M:%S',
    format='%(asctime)s [%(levelname)s] %(message)s'
)

日志 = logging.getLogger(__name__)

各识别码 = 唯一识别码()
收到回复 = asyncio.Event()
请求前缀 = "请求:"
回复前缀 = "回复:"
客户端连接 = None
收发特征 = None

def 匹配服务识别码(设备: BLEDevice, adv: AdvertisementData):
    服务识别码 = 各识别码.服务识别码.lower()
    广播服务识别码 = [uuid.lower() for uuid in adv.service_uuids]
    if 服务识别码 in 广播服务识别码:
        日志.info(f"Found matching device by service UUID: {设备.name} ({设备.address})")
        return True

    广播名称 = adv.local_name or 设备.name
    if 广播名称 == 各识别码.设备名称:
        日志.info(f"Found matching device by name: {广播名称} ({设备.address})")
        return True

    return False


def 处理通知(sender, 数据):
    内容 = 数据.decode('utf-8').strip()
    日志.info(f"Received data: {内容}")

    if 内容.startswith(请求前缀):
        路径 = 内容.removeprefix(请求前缀).strip()
        回复 = '存在' if Path(路径).exists() else '不存在'
        asyncio.create_task(客户端连接.write_gatt_char(收发特征, (回复前缀 + 回复).encode("utf-8")))
        日志.info(f"Response sent: {回复}")
    elif 内容.startswith(回复前缀):
        日志.info(f"Received response: {内容.removeprefix(回复前缀)}")
        收到回复.set()
    else:
        日志.warning(f"Unknown message: {内容}")

async def 中():
    try:
        # Search for devices and check if they match the UUID
        设备 = await BleakScanner.find_device_by_filter(匹配服务识别码, timeout=20)
        日志.info("Device search completed.")
        if 设备 is None:
            raise RuntimeError("No matching device found.")

        # Create a BleakClient instance and connect, then perform read/write operations
        async with BleakClient(设备) as 客户端:
            global 客户端连接, 收发特征
            客户端连接 = 客户端
            日志.info("Connected to the device.")
            服务 = 客户端.services.get_service(各识别码.服务识别码)
            日志.info(f"Service {服务} retrieved.")

            # Receive Bluetooth serial port information
            特征 = 服务.get_characteristic(各识别码.特征识别码)
            收发特征 = 特征
            日志.info(f"Characteristic {特征} retrieved.")

            await 客户端.start_notify(特征, 处理通知)
            日志.info("Notification started.")

            while True:
                路径 = await asyncio.to_thread(input, "请输入要让对端检查的路径（直接回车退出）：")
                路径 = 路径.strip()
                if not 路径:
                    break

                收到回复.clear()
                await 客户端.write_gatt_char(特征, (请求前缀 + 路径).encode("utf-8"))
                日志.info("Path written to characteristic.")
                try:
                    await asyncio.wait_for(收到回复.wait(), timeout=10)
                except asyncio.TimeoutError:
                    日志.warning("No response received within 10 seconds.")

    except Exception as e:
        日志.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(中())
