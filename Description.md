# CNC Serial Communicator

## Overview

The CNC Serial Communicator is a PyQt6-based GUI application designed to facilitate communication with CNC machines via a serial port. The application allows users to configure serial port settings, select and send CNC program files, receive data from the CNC machine, and save the received data.

## Dependencies

- Python 3.x
- PyQt6
- pyserial

## Features

- **Serial Port Configuration**: Configure serial port settings including port, baud rate, data bits, stop bits, parity, and flow control.
- **Open/Close Serial Port**: Open and close the serial port with the configured settings.
- **File Selection**: Select a CNC program file to be sent over the serial port.
- **Send File**: Send the selected CNC program file over the serial port.
- **Receive Data**: Receive data from the CNC machine and display it in the application.
- **Save Received Data**: Save the received data to a file.

## Requirements

- Python 3.x
- PyQt6
- pyserial

## Constraints

- The application assumes that the CNC machine is connected to one of the available serial ports.
- The application supports common serial port settings but may need adjustments for specific CNC machine configurations.
- The file selection dialog filters for CNC program files with extensions `.nc` and `.txt`.

## Installation

1. Install the required packages:
    ```sh
    pip install PyQt6 pyserial
    ```

2. Run the application:
    ```sh
    python cnc_serial_app.py
    ```

## Usage

1. **Open the application**: Run the `cnc_serial_app.py` script to open the GUI.
2. **Configure serial port settings**: Use the combo boxes to select the desired serial port settings.
3. **Open the serial port**: Click the "Open Serial Port" button to open the serial port with the selected settings.
4. **Select a file**: Click the "Select File" button to open a file dialog and select a CNC program file.
5. **Send the file**: Click the "Send File" button to send the selected file over the serial port.
6. **Receive data**: Click the "Receive Data" button to receive data from the CNC machine and display it in the text edit widget.
7. **Save received data**: Click the "Save Received Data" button to open a file dialog and save the received data to a file.
8. **Close the serial port**: Click the "Close Serial Port" button to close the serial port.

## Summary

The CNC Serial Communicator provides a user-friendly interface for configuring serial port settings, selecting and sending CNC program files, receiving data from the CNC machine, and saving the received data. It leverages PyQt6 for the GUI and pyserial for serial communication, making it a versatile tool for CNC machine operators and developers.