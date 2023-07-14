from pymodbus.client import ModbusSerialClient as ModbusClient
import ACREL_REGISTERS as Registers
import ACREL_FUNCTIONS as acrel
import schedule
import time

client_ACREL = None 
device_address =1  

def connection_Modbus():
    global client_ACREL
    try:
        if client_ACREL is None:
            print("client acrel is none")
        
        if client_ACREL is None or not client_ACREL.is_socket_open():
            client_ACREL = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=9600)
            client_ACREL.connect()
            print("estableciendo conexion: "+str(client_ACREL.is_socket_open()))
            
        if client_ACREL.is_socket_open():
            acrel.read_registers(client_ACREL,device_address,Registers.REGISTERS_LIST)
            #print("Reading data from sensor "+str(device_address))
            time.sleep(0.5)
           
        else:
            print("connection is closed and can't read the data from sensor")

       
    except Exception as e:
        print("Connection error: "+str(e))
       


if __name__ == "__main__":

    
    schedule.every(10).seconds.do(connection_Modbus)

    while 1:
    
        schedule.run_pending()
        time.sleep(0.5)
    
 