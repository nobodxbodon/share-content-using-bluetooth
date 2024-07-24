### Expected Operation
Behavioral Expectations:
First, start the server on Machine A, then start the client on Machine B, ensuring that the Bluetooth on both machines is available.
**Detailed Operation of Machine A's server.py:**
1. Import necessary modules and libraries: This includes `sys`, `asyncio`, `threading`, and relevant classes and functions from the `bless` library.
2. Define a synchronization trigger: Use `threading.Event` or `asyncio.Event` as the trigger based on the operating system type.
3. Define a write request handler function:
   `write_request`: Sets a new value for the characteristic and prints the received string.
4. Define an asynchronous run function `run`:
   - Clear the trigger.
   - Instantiate `BlessServer` and set the write request handler functions.
   - Add services and characteristics.
   - Start the server and wait for the trigger event.
   - Stop the server.
5. Run the event loop: Get the event loop and run the `run` function until completion.
   **The main purpose of this code is to create a BLE server that can execute the defined handler function upon receiving a write request, printing the received string.**
**Detailed Operation of Machine B's client.py:**
1. Import necessary libraries: Import `asyncio` and relevant modules from the `bleak` library.
2. Define constants: Define the service UUID and characteristic UUID.
3. Define a matching function: The `match_service_uuid` function checks if the scanned devices contain the specified service UUID.
4. Define the main function `main`:
   - Use `BleakScanner` to scan for Bluetooth devices and filter them through `match_service_uuid`.
   - Once a matching device is found, use `BleakClient` to connect to the device.
   - After a successful connection, get the service and characteristic, and write data ("吃了吗") to the characteristic.
   **The main purpose of this code is to scan and connect to a specific Bluetooth device via the service UUID and then send data to Machine A.**
**Summary of Machine A's Behavior:**
Create and configure the server object (mainly for service uuid, characteristic uuid, and read/write permissions)
Start the server thread and use the trigger to block the main thread to prevent it from automatically closing after execution, which would force the server thread to exit
Print all received strings
**Summary of Machine B's Behavior:**
Create and configure the client object (this step includes connecting to Machine A, searching and connecting via the service uuid)
Once connected, immediately write "吃了吗" to Machine A
End of the program
