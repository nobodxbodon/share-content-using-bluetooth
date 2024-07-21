import asyncio
from bleak import BleakScanner, BleakClient, BLEDevice, AdvertisementData

SERVICE_UUID = "A07498CA-AD5B-474E-940D-16F1FBE7E8CD"
CHAR_UUID = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"


def match_service_uuid(device: BLEDevice, adv: AdvertisementData):
    if SERVICE_UUID.lower() in adv.service_uuids:
        return True
    return False


async def main():
    # 搜索设备, 查看是否匹配NUS UUID，找到后可尝试建立连接，进行读写。
    device = await BleakScanner.find_device_by_filter(match_service_uuid, timeout=1000)

    # 创建BleakClient客户端，连接后进行串口操作
    async with BleakClient(device) as client:
        # await client.start_notify(CHAR_UUID,)

        print("Connected")

        # loop = asyncio.get_running_loop()
        service = client.services.get_service(SERVICE_UUID)
        # 接收蓝牙串口信息
        char = service.get_characteristic(CHAR_UUID)
        await client.write_gatt_char(char, "吃了吗".encode("utf-8"))


asyncio.run(main())
