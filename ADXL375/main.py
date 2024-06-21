from machine import Pin, I2C
import utime
import ustruct
import select, sys

ADXL375_ADDRESS = 0x53 # I2C 地址
ADXL375_OFSX = 0x1E # 0x1E-0x20 为加速度偏移量寄存器
ADXL375_BW_RATE = 0x2C # 加速度采样频率
ADXL375_POWER_CTL = 0x2D # 传感器电源模式
ADXL375_DATA_FORMAT = 0x31 # 加速度值的格式
ADXL375_DATAX0 = 0x32 # 0x32-0x37 为加速度寄存器
ADXL375_MULTIPLIER: float = 0.049

# 初始化 I2C LED
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
led = Pin("LED", Pin.OUT)
# USB 串口
poll_obj = select.poll()
poll_obj.register(sys.stdin, 1)

# 初始化 ADXL375
def init_ADXL375():
    i2c.writeto_mem(ADXL375_ADDRESS, ADXL375_POWER_CTL, bytearray([0x08]))  # measurement mode
    i2c.writeto_mem(ADXL375_ADDRESS, ADXL375_BW_RATE, bytearray([0x0D]))  # 800Hz
    i2c.writeto_mem(ADXL375_ADDRESS, ADXL375_DATA_FORMAT, bytearray([0x0B]))
    calibrate()

# 读取加速度寄存器
def read_raw():
    data = i2c.readfrom_mem(ADXL375_ADDRESS, ADXL375_DATAX0, 6)
    x, y, z = ustruct.unpack('<hhh', data)
    return x, y, z

# 读取加速度
def read_accel_data():
    x, y, z = read_raw()
    x = x * ADXL375_MULTIPLIER
    y = y * ADXL375_MULTIPLIER
    z = z * ADXL375_MULTIPLIER
    return x, y, z

# 校准
def calibrate():
    i2c.writeto_mem(ADXL375_ADDRESS, ADXL375_OFSX, bytearray([0, 0, 0]))
    utime.sleep_ms(50)
    x, y, z = read_raw()
    x_offset = round(-x / 4)
    y_offset = round(-y / 4)
    z_offset = round(-(z - 20) / 4)
    i2c.writeto_mem(ADXL375_ADDRESS, ADXL375_OFSX, ustruct.pack('bbb', x_offset, y_offset, z_offset))
    return x_offset, y_offset, z_offset

def main():
    init_ADXL375()
    start_ms = utime.ticks_ms()
    while True:
        led.toggle()
        utime.sleep_ms(1)
        try:
            x, y, z = read_accel_data()
            print(f"{x},{y},{z},{utime.ticks_ms() - start_ms}")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    main()
