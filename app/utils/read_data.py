import datetime
import serial
from utils.com_reader_client import com_reader_client

ser = serial.Serial(
    port='COM4',        # Replace with your COM port
    baudrate=9600,      # Baud rate
    bytesize=serial.EIGHTBITS,  # Data bits (8)
    parity=serial.PARITY_NONE,  # No parity
    stopbits=serial.STOPBITS_ONE,  # Stop bit (1)
    timeout=1           # Read timeout in seconds
)

def parse_voltages(data):
    voltages = []
    for i in range(0, len(data), 2):
        voltage_hex = data[i:i+2]
        voltage = int.from_bytes(voltage_hex, byteorder='big') / 1000.0
        # voltage = int(voltage_hex,16)
        voltages.append(voltage)
    return voltages

def parse_current(data):
    print("input curr", data ) 
    current_hex = data[:2]
    current = int.from_bytes(current_hex, byteorder='big') / 1000.0
    print("output curr", current ) 
    return current

def parse_temperatures(data):
    temperatures = []
    for i in range(0, len(data), 2):
        temp_hex = data[i:i+2]
        temp = int.from_bytes(temp_hex, byteorder='big') / 100.0
        temperatures.append(temp)
    return temperatures


def read_data(com_port, update_data_callback, selected_bank_number=1):
    # ser = com_reader_client(com_port)
    print(selected_bank_number)
    print("reading data from hardware....")
    if ser.in_waiting > 0:  # Check if there is data waiting to be read
        data = ser.read(140)  # Read all available data
        print(f"Raw data: {data}")
        
        start_idx = data.find(b'\x24')  # Locate the start character
        
        while start_idx != -1 and start_idx + 5 < len(data):
            print("inside while")
            bank_number = data[start_idx + 2]  # Battery Bank No
            print(bank_number)
            if bank_number == selected_bank_number:
                # Skip data if it doesn't match the selected bank number
                start_idx = data.find(b'\x24', start_idx + 1)
                continue

            voltage_start = data.find(b'\x56', start_idx)  # Locate 'V'
            current_start = data.find(b'\x41', voltage_start)  # Locate 'A'
            temperature_start = data.find(b'\x54', current_start)  # Locate 'T'
            
            if voltage_start != -1:
                voltage_data = data[voltage_start + 1 : current_start - 1]  # Adjust length based on observed data
                voltages = parse_voltages(voltage_data)
            
            if current_start != -1:
                current_data = data[current_start + 1 : current_start + 3]
                current = parse_current(current_data)
            
            if temperature_start != -1:
                temperature_data = data[temperature_start + 1 : temperature_start + 39]
                temperatures = parse_temperatures(temperature_data)
            
            timestamp = datetime.datetime.now()  # Get the current timestamp
            print(f"Received at {timestamp}: Bank {selected_bank_number}, Voltages: {voltages}, Current: {current}A, Temperatures: {temperatures}°C")
            
            # Now call update_data with all the required data
            update_data_callback(selected_bank_number, voltages, current, temperatures)
            
            start_idx = data.find(b'\x24', start_idx + 1)  # Look for the next start character in the remaining data

        print("out if")