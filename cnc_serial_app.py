import sys
import serial
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QComboBox, QLabel, QFormLayout, QPushButton, QFileDialog
from PyQt6.QtCore import Qt

class SerialApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ser = None  # Serial port object
        self.file_path = None  # Path to the selected file
        self.initUI()  # Initialize the UI

    def initUI(self):
        self.setWindowTitle('CNC Serial Communicator')  # Set window title
        self.setGeometry(100, 100, 1000, 800)  # Set window size and position

        central_widget = QWidget()  # Create central widget
        self.setCentralWidget(central_widget)  # Set central widget

        main_layout = QVBoxLayout(central_widget)  # Create main layout

        form_layout = QFormLayout()  # Create form layout for serial settings

        # Serial port selection
        self.port_combo = QComboBox()
        self.port_combo.addItems(['COM1', 'COM2', 'COM3'])
        form_layout.addRow(QLabel('Serial Port:'), self.port_combo)

        # Baud rate selection
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(['9600', '4800', '19200'])
        form_layout.addRow(QLabel('Baud Rate:'), self.baud_combo)

        # Data bits selection
        self.data_combo = QComboBox()
        self.data_combo.addItems(['7', '8'])
        form_layout.addRow(QLabel('Data Bits:'), self.data_combo)

        # Stop bits selection
        self.stop_combo = QComboBox()
        self.stop_combo.addItems(['1', '2'])
        form_layout.addRow(QLabel('Stop Bits:'), self.stop_combo)

        # Parity selection
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(['None', 'Even', 'Odd'])
        form_layout.addRow(QLabel('Parity:'), self.parity_combo)

        # Flow control selection
        self.flow_combo = QComboBox()
        self.flow_combo.addItems(['None', 'XON/XOFF', 'RTS/CTS', 'DTR/DSR'])
        form_layout.addRow(QLabel('Flow Control:'), self.flow_combo)

        main_layout.addLayout(form_layout)  # Add form layout to main layout

        button_layout = QVBoxLayout()  # Create layout for buttons

        # Button to open serial port
        self.open_button = QPushButton('Open Serial Port')
        self.open_button.clicked.connect(self.open_serial_port)
        button_layout.addWidget(self.open_button)

        # Button to close serial port
        self.close_button = QPushButton('Close Serial Port')
        self.close_button.clicked.connect(self.close_serial_port)
        button_layout.addWidget(self.close_button)

        # Button to select file
        self.file_button = QPushButton('Select File')
        self.file_button.clicked.connect(self.select_file)
        button_layout.addWidget(self.file_button)

        # Button to send file
        self.send_button = QPushButton('Send File')
        self.send_button.clicked.connect(self.send_file)
        button_layout.addWidget(self.send_button)

        # Button to receive data
        self.receive_button = QPushButton('Receive Data')
        self.receive_button.clicked.connect(self.receive_data)
        button_layout.addWidget(self.receive_button)

        # Button to save received data
        self.save_button = QPushButton('Save Received Data')
        self.save_button.clicked.connect(self.save_received_data)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)  # Add button layout to main layout

        # Text edit to display file content
        self.file_display = QTextEdit()
        self.file_display.setReadOnly(True)  # Make it read-only
        main_layout.addWidget(self.file_display)

        # Text edit for logging messages
        self.text_edit = QTextEdit()
        main_layout.addWidget(self.text_edit)

        self.show()  # Show the main window

    def open_serial_port(self):
        port = self.port_combo.currentText()  # Get selected port
        baudrate = int(self.baud_combo.currentText())  # Get selected baud rate
        databits = int(self.data_combo.currentText())  # Get selected data bits
        stopbits = int(self.stop_combo.currentText())  # Get selected stop bits
        parity_str = self.parity_combo.currentText()  # Get selected parity
        flow = self.flow_combo.currentText()  # Get selected flow control

        # Map parity string to serial module constant
        parity = serial.PARITY_NONE
        if parity_str == 'Even':
            parity = serial.PARITY_EVEN
        elif parity_str == 'Odd':
            parity = serial.PARITY_ODD

        try:
            # Open serial port with selected settings
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=databits,
                stopbits=stopbits,
                parity=parity,
                xonxoff=(flow == 'XON/XOFF')
            )
            self.text_edit.append(f"Serial port {port} opened with settings: {self.ser.get_settings()}")
        except serial.SerialException as e:
            self.text_edit.append(f"Error opening serial port {port}: {e}")
        except ValueError as e:
            self.text_edit.append(f"Invalid serial port settings: {e}")
        except Exception as e:
            self.text_edit.append(f"An unexpected error occurred: {e}")

    def close_serial_port(self):
        if self.ser and self.ser.is_open:
            try:
                self.ser.close()  # Close the serial port
                self.text_edit.append("Serial port closed.")
            except serial.SerialException as e:
                self.text_edit.append(f"Error closing serial port: {e}")
            except Exception as e:
                self.text_edit.append(f"An unexpected error occurred: {e}")
        else:
            self.text_edit.append("Serial port is not open.")

    def select_file(self):
        file_dialog = QFileDialog()
        # Open file dialog to select a CNC program file
        file_path, _ = file_dialog.getOpenFileName(self, 'Select CNC Program File', '', 'CNC Files (*.nc *.txt);;All Files (*)')
        if file_path:
            self.file_path = file_path  # Store selected file path
            self.text_edit.append(f"File selected: {file_path}")
            try:
                # Read and display the file content
                with open(file_path, 'r') as file:
                    self.file_display.setPlainText(file.read())
            except Exception as e:
                self.file_display.setPlainText(f"Error reading file: {e}")

    def send_file(self):
        if self.ser and self.ser.is_open and self.file_path:
            try:
                # Read and send the file content over serial port
                with open(self.file_path, 'rb') as file:
                    data = file.read()
                    self.ser.write(data)
                self.text_edit.append(f"File '{self.file_path}' sent successfully.")
            except FileNotFoundError:
                self.text_edit.append(f"Error: File '{self.file_path}' not found.")
            except PermissionError:
                self.text_edit.append(f"Error: Permission denied to read file '{self.file_path}'.")
            except serial.SerialTimeoutException:
                self.text_edit.append("Error: Serial port timeout during transmission.")
            except serial.SerialException as e:
                self.text_edit.append(f"Error: Serial port error during transmission: {e}")
            except Exception as e:
                self.text_edit.append(f"An unexpected error occurred: {e}")
        else:
            self.text_edit.append("Serial port not open or no file selected.")

    def receive_data(self):
        if self.ser and self.ser.is_open:
            try:
                if self.ser.in_waiting > 0:
                    # Read and display the received data
                    data = self.ser.read(self.ser.in_waiting)
                    self.file_display.setPlainText(data.decode())
                    self.text_edit.append(f"Received data: {data}")
                else:
                    self.text_edit.append("No data available to receive.")
            except serial.SerialTimeoutException:
                self.text_edit.append("Error: Serial port timeout during reception.")
            except serial.SerialException as e:
                self.text_edit.append(f"Error receiving data: {e}")
            except Exception as e:
                self.text_edit.append(f"An unexpected error occurred: {e}")
        else:
            self.text_edit.append("Serial port not open.")

    def save_received_data(self):
        file_dialog = QFileDialog()
        # Open file dialog to save received data
        file_path, _ = file_dialog.getSaveFileName(self, 'Save Received Data', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            try:
                # Save the received data to the selected file
                with open(file_path, 'w') as file:
                    file.write(self.file_display.toPlainText())
                self.text_edit.append(f"Received data saved to: {file_path}")
            except Exception as e:
                self.text_edit.append(f"Error saving received data: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)  # Create the application
    ex = SerialApp()  # Create the main window
    sys.exit(app.exec())  # Run the application