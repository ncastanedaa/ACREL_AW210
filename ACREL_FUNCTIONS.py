import ACREL_REGISTERS as Registers
from datetime import datetime
from threading import Thread
import time
import struct


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
    
def read_value(client,device_address,variable):
    try:
        reg= client.read_holding_registers(slave=device_address,address=variable,count=2)
        if reg.isError():
            print(reg.__str__())
            return False,"-1"
        else:
            coded_values = reg.registers
            value_hex_1 = hex(coded_values[0])[2:]
            value_hex_2 = hex(coded_values[1])[2:]
            value_hex_1 = pad_hex_string(value_hex_1,4)
            value_hex_2 = pad_hex_string(value_hex_2,4)
            value_hex=value_hex_1+value_hex_2
            value = round(hex_to_float(value_hex),2)
                
            print(value)    
            return True,value       
    except Exception as e:
        print("error"+str(e))

def read_value_harmonics(client,device_address,variable):
    try:
        reg= client.read_holding_registers(slave=device_address,address=variable,count=1)
        if reg.isError():
            print(reg.__str__())
            return False,"-1"
        else:
            val = reg.registers[0]
            value = val/100
            print(value)
            return True, value       
    except Exception as e:
        print("error"+str(e))



def read_registers(client,device_address,registers_dictionary):
    """Read the registers and store the values in a dictionary with the form variable:value. Then return the dictionary."""
    index = 0
    list_key = list(registers_dictionary)
    error_counter = 0
    can_continue = True 

    while index < len(list_key) and can_continue:

        if len(registers_dictionary[list_key[index]]) > 1 :

            #variable = "{name}".format(name=list_key[index])
            sensor_response = read_value(client, device_address, registers_dictionary[list_key[index]][0])

            if sensor_response[0]:
                message = "{name}".format(name=list_key[index])
                print(message," ",sensor_response)
                index +=1 
                error_counter = 0
      
            else: 
                error_counter +=1
                time.sleep(0.2)
            if error_counter == 4:
                can_continue = False
                index +=1
                
        
        # This secctions read harmonics values
        if len(registers_dictionary[list_key[index]]) == 1 :

            sensor_response = read_value_harmonics(client,device_address,registers_dictionary[list_key[index]][0])
            if sensor_response[0]:
                message = "{name}".format(name=list_key[index])
                print(message," ",sensor_response)
                index +=1 
                error_counter = 0
            else: 
                error_counter +=1
                time.sleep(0.2)
            if error_counter == 4:
                can_continue = False
                index +=1
                

    