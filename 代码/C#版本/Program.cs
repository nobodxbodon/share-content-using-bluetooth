// https://www.csharp.com/article/transferring-data-via-bluetooth-in-net/

using InTheHand.Net;
using InTheHand.Net.Bluetooth;
using InTheHand.Net.Sockets;

class Program
{
  static void Main(string[] args)
  {

    // Discover nearby Bluetooth devices

    BluetoothClient bluetoothClient = new BluetoothClient();
    BluetoothDeviceInfo[] devices = bluetoothClient.DiscoverDevices();

    Console.WriteLine("Discovered Bluetooth Devices:");
    foreach (BluetoothDeviceInfo device in devices)
    {
      Console.WriteLine($"Device Name: {device.DeviceName}");
      Console.WriteLine($"Device Address: {device.DeviceAddress}");
      Console.WriteLine($"Is Connected: {device.Connected}");
      Console.WriteLine();
    }

    //   output Device Address : 8803E9C06F34;

    //  Convert this to 88:03:E9:C0:6F:34

    BluetoothAddress deviceAddress = BluetoothAddress.Parse("88:03:E9:C0:6F:34");
    BluetoothEndPoint endPoint = new BluetoothEndPoint(deviceAddress, BluetoothService.SerialPort);
    BluetoothClient client = new BluetoothClient();

    try
    {
      client.Connect(endPoint);

      if (client.Connected)
      {
        Console.WriteLine("Connected to the Bluetooth device!");

        NetworkStream stream = client.GetStream();
        string dataToSend = "Hello, Bluetooth!";
        byte[] dataBytes = Encoding.UTF8.GetBytes(dataToSend);
        stream.Write(dataBytes, 0, dataBytes.Length);

        Console.WriteLine("Data sent successfully.");

        // Receiving data
        byte[] receiveBuffer = new byte[1024];
        int bytesRead = stream.Read(receiveBuffer, 0, receiveBuffer.Length);
        string receivedData = Encoding.UTF8.GetString(receiveBuffer, 0, bytesRead);

        Console.WriteLine($"Received data: {receivedData}");
      }
      else
      {
        Console.WriteLine("Connection failed.");
      }
    }
    catch (Exception ex)
    {
      Console.WriteLine($"Error connecting to the device: {ex.Message}");
    }
  }
}