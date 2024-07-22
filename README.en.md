# Share Contents using Bluetooth

### Description

Sharing text contents through bluetooth instead of network.

Technical research while building prototype step by step. Details see [bounty tasks](https://gitee.com/zhishi/share-content-using-bluetooth/issues)

Progress:

1. [Transfer text between two Win10 systems](https://gitee.com/zhishi/share-content-using-bluetooth/issues/IABP3R)

### Reference

- [Briar](https://briarproject.org/)

### Expected Operation

Behavioral Expectations:
First, start the server on Machine A, then start the client on Machine B, ensuring that the Bluetooth on both machines is available.
**Detailed Operation of Machine A's server.py:**
1. Import necessary modules and libraries: This includes `sys`, `asyncio`, `threading`, and relevant classes and functions from the `bless` library.
2. Define a synchronization trigger: Use `threading.Event` or `asyncio.Event` as the trigger based on the operating system type.
3. Define read and write request handling functions:
   - `read_request`: Returns the current value of the characteristic.
   - `write_request`: Sets a new value for the characteristic and triggers an event upon receiving the specific string "吃了吗".
4. Define the asynchronous running function `run`:
   - Clear the trigger.
   - Instantiate `BlessServer` and set the read and write request handling functions.
   - Add services and characteristics.
   - Start the server and wait for the trigger event.
   - Stop the server.
5. Run the event loop: Get the event loop and run the `run` function until completion.
**The main purpose of this code is to create a BLE server that can execute defined processing functions upon receiving read and write requests. When a "write" request is triggered, it checks if the written value is "吃了吗". If so, it controls the trigger to unblock the main thread, ending the program.**
**Detailed Operation of Machine B's client.py:**
1. Import necessary libraries: Import `asyncio` and relevant modules from the `bleak` library.
2. Define constants: Define the service UUID and characteristic UUID.
3. Define the matching function: `match_service_uuid` is used to check if the scanned devices contain the specified service UUID.
4. Define the main function `main`:
   - Use `BleakScanner` to scan for Bluetooth devices and filter them through `match_service_uuid`.
   - Once a matching device is found, use `BleakClient` to connect to the device.
   - After a successful connection, get the service and characteristic, and write data ("吃了吗") to the characteristic.
**The main purpose of this code is to scan and connect to a specific Bluetooth device through the service's UUID and then send data to Machine A.**
**Summary of Machine A's Behavior:**
Create and configure the server object (mainly for service UUID, characteristic UUID, and read/write permissions).
Start the server thread and use the trigger to block the main thread to prevent it from automatically closing after execution, which would force the server thread to exit.
The main thread is blocked by the trigger until the server thread receives content and checks it. If the check is "吃了吗", the trigger blocking the main thread is closed.
Since the main thread is no longer blocked, the program immediately proceeds to the end and terminates.
**Summary of Machine B's Behavior:**
Create and configure the client object (this step includes connecting to Machine A by searching and connecting through the service's UUID).
Once connected, immediately write "吃了吗" to Machine A.
The program ends.
