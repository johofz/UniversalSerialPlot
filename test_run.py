import asyncio
from bleak import BleakClient

device_address = "C3:4E:74:3C:93:48"  # Die MAC-Adresse deines Geräts

async def list_services(address):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid}, Eigenschaften: {characteristic.properties}")

asyncio.run(list_services(device_address))
