from serial import Serial
import time

# 设置串口参数
ser = Serial('COM3', 115200)
now = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())

with open(f'accel-{now}.csv', 'w', encoding='utf-8') as file:
    file.write('x-axis,y-axis,z-axis,time\n')
    while True:
        # 读取串口数据
        data = ser.readline().decode('utf-8').strip()
        if not data:
            break  # 如果没有数据，退出循环
        # 写入文件
        file.write(data + '\n')

# 关闭串口
ser.close()
