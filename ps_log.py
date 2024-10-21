# This script connects via serial to an embedded Linux device and continuously 
# checks the running processes, writing them out to a txt file.

# serial and time packages are required (install serial with "pip3 install pyserial")
import serial
import time

def get_serial_port(port_num):
    """
    Construct the port path based on the user's input number.
    Example: Input '0' -> '/dev/ttyUSB0'
    """
    return f"/dev/ttyUSB{port_num}"

# Get user input for the port number and baud rate.
port_num = input("Enter the port number (e.g., 0 for /dev/ttyUSB0): ")
baud_rate = input("Enter the baud rate (e.g., 115200): ")

# Construct the full port path.
port = get_serial_port(port_num)

try:
    # Open the serial connection using the user-supplied port and baud rate.
    serial_port = serial.Serial(
        port=port,
        baudrate=int(baud_rate),
        bytesize=8,
        timeout=1,
        stopbits=serial.STOPBITS_ONE
    )

    print(f"Connected to {port} at {baud_rate} baud.")
except serial.SerialException as e:
    print(f"Failed to connect to {port}: {e}")
    exit(1)

# Empty string to hold serial reads
serial_string = ""

# Continuously read and write while the script is running
while True:
    try:
        # Wait 10 seconds between writes
        time.sleep(10)

        # Send the 'ps' command to the device
        serial_port.write(b"ps \r\b")

        # Read from the serial port until "ps" is found in the output
        serial_string = serial_port.read_until(b"ps")

        # Print the output (decoded from bytes to ASCII)
        output = serial_string.decode("Ascii", errors="ignore")
        print(output)

        # Write all output to a log file
        with open("ps_log.txt", "a") as f:
            f.write(output + "\n")

        print("Waiting 10 Seconds...")

    except Exception as e:
        print(f"An error occurred: {e}")
        break

# Close the serial port on exit
serial_port.close()
print("Serial connection closed.")