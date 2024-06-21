using System.IO.Ports;
using System.Text;

string filePath = Path.Combine(Environment.CurrentDirectory, $"accel-{DateTime.Now.ToString("yyyy-MM-dd-HH-mm-ss")}.csv");
using StreamWriter sw = new StreamWriter(File.Create(filePath, 4096));
sw.WriteLine("x-axis,y-axis,z-axis,time");

using SerialPort sp = new SerialPort(portName: "COM24")
{
    BaudRate = 115200,
    Encoding = Encoding.UTF8,
    ReadTimeout = 500
};

Console.WriteLine("按任意键退出...");

sp.Open();

while (!Console.KeyAvailable)
{
    string content = sp.ReadLine();
    sw.WriteLine(content);
    Console.WriteLine(content);
}

sp.Close();
