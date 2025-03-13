import sys
import serial
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QComboBox, QLabel, QFormLayout, QPushButton, QFileDialog
from PyQt6.QtCore import Qt

class SerialApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ser = None
        self.file_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('CNC Serial Communicator')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        form_layout = QFormLayout()

        self.port_combo = QComboBox()
        self.port_combo.addItems(['COM1', 'COM2', 'COM3'])
        form_layout.addRow(QLabel('Serial Port:'), self.port_combo)

        self.baud_combo = QComboBox()
        self.baud_combo.addItems(['9600', '4800', '19200'])
        form_layout.addRow(QLabel('Baud Rate:'), self.baud_combo)

        self.data_combo = QComboBox()
        self.data_combo.addItems(['7', '8'])
        form_layout.addRow(QLabel('Data Bits:'), self.data_combo)

        self.stop_combo = QComboBox()
        self.stop_combo.addItems(['1', '2'])
        form_layout.addRow(QLabel('Stop Bits:'), self.stop_combo)

        self.parity_combo = QComboBox()
        self.parity_combo.addItems(['None', 'Even', 'Odd'])
        form_layout.addRow(QLabel('Parity:'), self.parity_combo)

        self.flow_combo = QComboBox()
        self.flow_combo.addItems(['None', 'XON/XOFF', 'RTS/CTS', 'DTR/DSR'])
        form_layout.addRow(QLabel('Flow Control:'), self.flow_combo)

        layout.addLayout(form_layout)

        self.open_button = QPushButton('Open Serial Port')
        self.open_button.clicked.connect(self.open_serial_port)
        layout.addWidget(self.open_button)

        self.close_button = QPushButton('Close Serial Port')
        self.close_button.clicked.connect(self.close_serial_port)
        layout.addWidget(self.close_button)

        self.file_button = QPushButton('Select File')
        self.file_button.clicked.connect(self.select_file)
        layout.addWidget(self.file_button)

        self.send_button = QPushButton('Send File')
        self.send_button.clicked.connect(self.send_file)
        layout.addWidget(self.send_button)

        self.receive_button = QPushButton('Receive Data')
        self.receive_button.clicked.connect(self.receive_data)
        layout.addWidget(self.receive_button)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.show()

    def open_serial_port(self):
        port = self.port_combo.currentText()
        baudrate = int(self.baud_combo.currentText())
        databits = int(self.data_combo.currentText())
        stopbits = int(self.stop_combo.currentText())
        parity_str = self.parity_combo.currentText()
        flow = self.flow_combo.currentText()

        parity = serial.PARITY_NONE
        if parity_str == 'Even':
            parity = serial.PARITY_EVEN
        elif parity_str == 'Odd':
            parity = serial.PARITY_ODD

        try:
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
                self.ser.close()
                self.text_edit.append("Serial port closed.")
            except serial.SerialException as e:
                self.text_edit.append(f"Error closing serial port: {e}")
            except Exception as e:
                self.text_edit.append(f"An unexpected error occurred: {e}")
        else:
            self.text_edit.append("Serial port is not open.")

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Select CNC Program File', '', 'CNC Files (*.nc *.txt);;All Files (*)')
        if file_path:
            self.file_path = file_path
            self.text_edit.append(f"File selected: {file_path}")

    def send_file(self):
        if self.ser and self.ser.is_open and self.file_path:
            try:
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
                    data = self.ser.read(self.ser.in_waiting)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SerialApp()
    sys.exit(app.exec())