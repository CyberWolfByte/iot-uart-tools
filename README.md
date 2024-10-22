# **Automating Serial Connections with Python**
Python scripts can be used to connect to UART serial interfaces and automate interactions with embedded Linux devices like the TP-Link WR841N router. Automating tasks such as process monitoring or interrupting boot sequences helps in vulnerability analysis and testing.

## **Python Scripts Features**
- **`ps_log.py`**: This script connects to the serial interface of the router and continuously logs running processes to a text file (`ps_log.txt`). This is useful for monitoring the router’s operations and identifying suspicious activities.
- **`boot_interrupt_v2.py`**: This script connects to the router’s UART shell and sends commands to reboot the device and interrupt the bootloader process. If the `MT7628` shell is captured, the script switches to interactive mode to allow further manual interaction with the router. While the WR841N bootloader is locked down, this script demonstrates how such an interaction could work if full U-Boot functionality were available.

## **Target** 
- **Manufacturer**: TP-Link
- **Version**: 14.6
- **Model Number**: TL-WR841N(US)
- **Serial Number**: Y224032004449
- **FCC ID**: TE7WR841NV14
- **CPU**: Mediatek MT7628NN
- **RAM**: Zentel A3S56D40GTP -50L
- **ROM**: cFeon QH32B-104HIP
