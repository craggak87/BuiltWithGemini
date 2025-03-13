# CNC Serial Communicator

## Description

The CNC Serial Communicator is a PyQt6-based GUI application designed to facilitate communication with CNC machines via a serial port. The application allows users to configure serial port settings, select and send CNC program files, receive data from the CNC machine, and save the received data.

## Setup Instructions

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/cnc-serial-communicator.git
    cd cnc-serial-communicator
    ```

2. **Install the required packages**:
    ```sh
    pip install PyQt6 pyserial
    ```

3. **Run the application**:
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

## Contributor Guidelines

We welcome contributions to the CNC Serial Communicator project! To contribute, please follow these steps:

1. **Fork the repository**: Click the "Fork" button at the top right of this page to create a copy of this repository in your GitHub account.
2. **Clone your fork**: Clone your forked repository to your local machine.
    ```sh
    git clone https://github.com/yourusername/cnc-serial-communicator.git
    cd cnc-serial-communicator
    ```
3. **Create a branch**: Create a new branch for your feature or bug fix.
    ```sh
    git checkout -b my-feature-branch
    ```
4. **Make your changes**: Make your changes to the codebase.
5. **Commit your changes**: Commit your changes with a descriptive commit message.
    ```sh
    git commit -m "Add new feature"
    ```
6. **Push to your fork**: Push your changes to your forked repository.
    ```sh
    git push origin my-feature-branch
    ```
7. **Create a pull request**: Open a pull request to the main repository, describing your changes and why they should be merged.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.