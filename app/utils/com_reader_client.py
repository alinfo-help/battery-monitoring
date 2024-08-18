import serial

def com_reader_client(com_port):
    try:
            ser = serial.Serial(
            port=com_port,        # Replace with your COM port
            baudrate=9600,      # Baud rate
            bytesize=serial.EIGHTBITS,  # Data bits (8)
            parity=serial.PARITY_NONE,  # No parity
            stopbits=serial.STOPBITS_ONE,  # Stop bit (1)
            timeout=1           # Read timeout in seconds
            )
            return ser
    except:
        print("Error in creating com_read client...")
    
