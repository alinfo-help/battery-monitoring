import serial
import csv

# Function to convert hex string to decimal value
def hex_to_decimal(hex_str):
    return int(hex_str, 16)

# Function to read and parse data from the serial port
def read_data_from_com(port='COM4', baudrate=9600, timeout=1):
    # Open the serial port
    ser = serial.Serial(port, baudrate, timeout=timeout)
    
    # Prepare CSV file to store the data
    with open('battery_data.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Bank No', 'Voltage', 'Current (A)', 'Temperature'])
        
        while True:
            line = ser.readline().decode('ascii', errors='ignore').strip()
            if line:
                if line.startswith('$'):  # Start character
                    bank_no = None
                    voltage = []
                    current = None
                    temperature = []

                    # Reading bank number
                    line = ser.readline().decode('ascii', errors='ignore').strip()
                    if line:
                        bank_no = hex_to_decimal(line.split()[2])
                    
                    # Reading voltage values
                    while True:
                        line = ser.readline().decode('ascii', errors='ignore').strip()
                        if line.startswith('V'):
                            voltage_value = float(line.split()[2]) / 1000  # Assuming the value is in mV
                            voltage.append(voltage_value)
                        else:
                            break
                    
                    # Reading current value
                    if line.startswith('A'):
                        current_value = float(line.split()[2]) / 1000  # Assuming the value is in mA
                        current = current_value
                    
                    # Reading temperature values
                    while True:
                        line = ser.readline().decode('ascii', errors='ignore').strip()
                        if line.startswith('T'):
                            temp_value = hex_to_decimal(line.split()[2])  # Assuming the temperature is in hex
                            temperature.append(temp_value)
                        else:
                            break

                    # Writing data to CSV
                    csv_writer.writerow([bank_no, voltage, current, temperature])

            # Break the loop when the end character is detected
            if line.endswith('#'):
                break

    ser.close()

# Call the function to start reading and storing data
read_data_from_com(port='COM4', baudrate=9600)