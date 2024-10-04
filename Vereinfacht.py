import asyncio
from bleak import BleakScanner, BleakClient

device_address = "0CF7B642-F1B0-9675-BE1D-4E6D244D8829"
# b088b5a1-08fe-4655-af55-1c69c8917659
# b088b5a2-08fe-4655-af55-1c69c8917659


async def discover_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Gerät gefunden: {device.name}, {device.address}")


asyncio.run(discover_devices())


async def list_services(address):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(
                    f"  Characteristic: {characteristic.uuid}, Eigenschaften: {characteristic.properties}")

asyncio.run(list_services(device_address))
