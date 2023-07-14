from pymodbus.client import ModbusSerialClient as ModbusClient
import time
import struct

# configure the serial port
#change port name if using windows to COM3 or the number you get in the device manager
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600)

#Here you set the modbus address of the device.

device_address = 1 

client.connect()

def hex_to_float(hex_string):
    # Convert hex string to bytes
    hex_bytes = bytes.fromhex(hex_string)
    
    # Unpack bytes as a float
    return struct.unpack('!f', hex_bytes)[0]

def pad_hex_string(hex_string, length):
    
    num_digits = len(hex_string)
    if num_digits < length:
        return hex_string.zfill(length)
    else:
        return hex_string

while 1:
    try:
        reg= client.read_holding_registers(slave=device_address,address=0x100, count=2)
        val = reg.registers
        a = hex(val[0])[2:]
        a = pad_hex_string(a,4)
        b = hex(val[1])[2:]
        b = pad_hex_string(b,4)
        hex_str = a+b
        value = hex_to_float(hex_str)
        print('raw registers data ',val,'converted float value ',round(value,2))
        
    except Exception as e:
        print(e)
    time.sleep(0.5)

client.close()
print("Connection closed!")