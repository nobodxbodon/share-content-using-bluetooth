import asyncio
import logging
from bleak import BleakScanner, BleakClient, BLEDevice, AdvertisementData
from the_uuids import UUID as UUIDs

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    datefmt='%H:%M:%S',
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)

uuids = UUIDs()

def match_service_uuid(device: BLEDevice, adv: AdvertisementData):
    if uuids.service_uuid.lower() in adv.service_uuids:
        logger.info(f"Found matching device: {device.name} ({device.address})")
        return True
    return False


def handle_notification(sender, data):
    logger.info(f"Received data: {data.decode('utf-8')}")

async def main():
    try:
        # Search for devices and check if they match the UUID
        device = await BleakScanner.find_device_by_filter(match_service_uuid, timeout=20)
        logger.info("Device search completed.")

        # Create a BleakClient instance and connect, then perform read/write operations
        async with BleakClient(device) as client:
            logger.info("Connected to the device.")
            service = client.services.get_service(uuids.service_uuid)
            logger.info(f"Service {service} retrieved.")

            # Receive Bluetooth serial port information
            char = service.get_characteristic(uuids.characteristic_uuid)
            logger.info(f"Characteristic {char} retrieved.")
            
            await client.start_notify(char, handle_notification)
            logger.info("Notification started.")

            await client.write_gatt_char(char, "吃了吗".encode("utf-8"))
            logger.info("Data written to characteristic.")

    except AttributeError:
        logger.error("No matching device found.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    asyncio.run(main())