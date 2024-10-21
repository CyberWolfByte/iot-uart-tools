# boot_interrupt_v2.py

import serial
import time

def get_serial_port(port_num):
    """
    Construct the port path based on the user's input number.
    Example: Input '0' -> '/dev/ttyUSB0'
    """
    return f"/dev/ttyUSB{port_num}"

# Get user input for port number and baud rate.
port_num = input("Enter the port number (e.g., 0 for /dev/ttyUSB0): ")
baud_rate = input("Enter the baud rate (e.g., 115200): ")

# Construct the full port path.
port = get_serial_port(port_num)

try:
    # Open the serial connection with user-specified parameters.
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

# Clear any cached data in the serial buffers.
serial_port.reset_output_buffer()
serial_port.reset_input_buffer()

# Send the reboot command and wait for it to take effect.
print("Sending reboot command...")
serial_port.write(b"reboot \r\b")
time.sleep(3)  # Adjust sleep time as required

# Track if the shell has been captured.
shell_captured = False

# Send the 'tpl' command repeatedly until the shell is captured or max attempts reached.
print("Attempting to interrupt the bootloader with 'tpl'...")
for i in range(100):
    if shell_captured:
        print("Shell prompt detected! Stopping further 'tpl' attempts.")
        break  # Stop sending 'tpl' commands if shell is captured.

    try:
        serial_port.write(b"tpl \r\b")
        print(f"Writing 'tpl' #: {i}")

        # Read from the serial port to check for the shell prompts.
        serial_string = serial_port.readline()
        output = serial_string.decode("Ascii", errors="ignore")
        print(output)

        # Detect if the shell prompt is captured.
        if "MT7628 #" in output:
            print("MT7628 shell prompt detected! Switching to interactive mode.")
            shell_captured = True  # Stop sending further 'tpl' commands.

    except Exception as e:
        print(f"Error during 'tpl' sending: {e}")
        break

# If the shell was captured, enter interactive mode.
if shell_captured:
    print("\nInteractive shell mode: You can now enter commands.")
    print("Type 'exit' to quit the interactive session.\n")

    try:
        while True:
            # Get user input for commands to send to the shell.
            user_input = input("MT7628 # ")
            if user_input.strip().lower() == "exit":
                print("Exiting interactive shell mode.")
                break

            # Send the user input to the shell.
            serial_port.write((user_input + "\r\n").encode())

            # Read and print the response from the shell.
            while True:
                response = serial_port.readline()
                if not response:
                    break  # Exit inner loop if no more data.
                print(response.decode("Ascii", errors="ignore"))

    except KeyboardInterrupt:
        print("\nUser interrupted the interactive session.")

# Ensure the serial port is closed on exit.
serial_port.close()
print("Serial connection closed.")