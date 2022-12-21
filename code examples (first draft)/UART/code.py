import time
import board
import busio
from adafruit_emc2101 import EMC2101
import digitalio

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

uart = busio.UART(board.GP0, board.GP1, baudrate=115200, timeout=0)
uart1 = busio.UART(board.GP8, board.GP9, baudrate=115200, timeout=0)
i2c = busio.I2C(board.GP5, board.GP4) 
emc = EMC2101(i2c)

while True:
    dataA = uart.read(8)
    dataB = uart1.read(8)
    #uart.write(bytes(str("Hello Blade A" + "\n"),'UTF-8'))
    #uart1.write(bytes(str("Hello Blade B" + "\n"),'UTF-8'))
    #print (dataA)
    #print (dataB)

    try:
        dataA=int(dataA)
    except:        
        dataA = 'Auto'
    try:
        dataB=int(dataB)
    except:        
        dataB = 'Auto'

#     if dataA is not None:
#         dataA = dataA.decode()
#     if dataB is not None:
#         dataB = dataB.decode()
    print("From Blade A", dataA)
    print("From Blade B", dataB)
    
    print("Blade A airflow temperature:", emc.external_temperature, "C")
    print("Blade B airflow temperature:", emc.internal_temperature, "C")
    BladeA_uart_info = bytes(str("Blade A airflow temperature: " + str(emc.external_temperature) + " C" + "\r\n"),'UTF-8')
    BladeB_uart_info = bytes(str("Blade B airflow temperature: " + str(emc.internal_temperature) + " C" + "\r\n"),'UTF-8')
    #BladeA_uart_info = bytes(str(str(emc.external_temperature) + " C" + "\r\n"),"ascii")
    #BladeB_uart_info = bytes(str(str(emc.internal_temperature) + " C" + "\r\n"),"ascii")
    #print(BladeA_uart_info + BladeB_uart_info)
    fan_speed=bytes(str("Fan speed: " + str(emc.fan_speed) + "RPM" + "\r\n" + "\r\n"),'UTF-8')
    blade_request=bytes(str("Blade A: " + str(dataA) + "%" + "| Blade B: " + str(dataB) + "%" + "\r\n"),'UTF-8')
    uart.write(BladeA_uart_info + BladeB_uart_info + blade_request + fan_speed)
    uart1.write(BladeA_uart_info + BladeB_uart_info + blade_request + fan_speed)
    
    if dataA is not 'Auto':
        led.value = True
        print("Set the speed as Blade A asks:", dataA, " %")
        emc.manual_fan_speed = int(dataA)
        time.sleep(1)
        print("Fan speed", emc.fan_speed, "RPM")
        time.sleep(1)
        
    if dataB is not 'Auto':
        led.value = True
        print("Set the speed as Blade B asks:", dataB, " %")
        emc.manual_fan_speed = int(dataB)
        time.sleep(2)
        print("Fan speed", emc.fan_speed, "RPM")
        time.sleep(10)    
    else:     
        if 40 <= emc.external_temperature or 40 <= emc.internal_temperature:
            led.value = True
            print("Setting fan speed to 100%")
            emc.manual_fan_speed = 100
            time.sleep(2)
            print("Fan speed", emc.fan_speed, "RPM")
            time.sleep(1)
        elif 35 <= emc.external_temperature < 40 or 35 <= emc.internal_temperature < 40:
            led.value = True
            print("Setting fan speed to 70%")
            emc.manual_fan_speed = 70
            time.sleep(2)
            print("Fan speed", emc.fan_speed, "RPM")
            time.sleep(1)
        elif 33 <= emc.external_temperature < 35 or 33 <= emc.internal_temperature < 35:
            led.value = True
            print("Setting fan speed to 60%")
            emc.manual_fan_speed = 60
            time.sleep(2)
            print("Fan speed", emc.fan_speed, "RPM")
            time.sleep(1)
        elif 31 <= emc.external_temperature < 33 or 31 <= emc.internal_temperature < 33:
            led.value = True
            print("Setting fan speed to 40%")
            emc.manual_fan_speed = 40
            time.sleep(2)
            print("Fan speed", emc.fan_speed, "RPM")
            time.sleep(1)
        elif 29 <= emc.external_temperature < 31 or 29 <= emc.internal_temperature < 31:
            led.value = True
            print("Setting fan speed to 30%")
            emc.manual_fan_speed = 30
            time.sleep(2)
            print("Fan speed", emc.fan_speed, "RPM")
            time.sleep(1)
        else:
            led.value = True
            print("Setting fan speed to 10%")
            emc.manual_fan_speed = 10
            time.sleep(2)
            print("Fan speed", emc.fan_speed, "RPM")
            time.sleep(1)
   
    print("")
    time.sleep(1)
