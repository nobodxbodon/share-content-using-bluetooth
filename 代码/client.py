import asyncio
import logging
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

def 匹配服务识别码(设备: BLEDevice, adv: AdvertisementData):
    if 各识别码.服务识别码.lower() in adv.service_uuids:
        日志.info(f"Found matching device: {设备.name} ({设备.address})")
        return True
    return False


def 处理通知(sender, 数据):
    日志.info(f"Received data: {数据.decode('utf-8')}")

async def 中():
    try:
        # Search for devices and check if they match the UUID
        设备 = await BleakScanner.find_device_by_filter(匹配服务识别码, timeout=20)
        日志.info("Device search completed.")

        # Create a BleakClient instance and connect, then perform read/write operations
        async with BleakClient(设备) as 客户端:
            日志.info("Connected to the device.")
            服务 = 客户端.services.get_service(各识别码.服务识别码)
            日志.info(f"Service {服务} retrieved.")

            # Receive Bluetooth serial port information
            特征 = 服务.get_characteristic(各识别码.特征识别码)
            日志.info(f"Characteristic {特征} retrieved.")
            
            await 客户端.start_notify(特征, 处理通知)
            日志.info("Notification started.")

            await 客户端.write_gatt_char(特征, "吃了吗".encode("utf-8"))
            日志.info("Data written to characteristic.")

    except AttributeError:
        日志.error("No matching device found.")
    except Exception as e:
        日志.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(中())