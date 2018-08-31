# Copyright (c) 2018 Kyle Lopin (Naresuan University) <kylel@nu.ac.th>

"""
File to communication with Cypress BLE
"""

import glob
import logging
import queue
import serial
import sys
import time
import threading

__author__ = 'Kyle Vitautas Lopin'

BAUDRATE = 115200
# BAUDRATE = 9600
# BAUDRATE = 114286
STOPBITS = serial.STOPBITS_ONE
PARITY = serial.PARITY_NONE
BYTESIZE = serial.EIGHTBITS

ID_MESSAGE = "BLE Initialized"


class IoTComm(object):
    def __init__(self, master):
        self.master = master
        self.found = False
        self.connected = False
        self.device = self.connect_usb()

        # make an extra thread to poll the usb as this thread will hang on the timeouts of the usb
        # self.data_ready_event = event
        # self.data_queue = queue
        # self.data_aquire_thread = ThreadedUSBDataCollector(self, master)

    def connect_usb(self):
        available_ports = find_available_ports()
        for port in available_ports:
            try:
                device = serial.Serial(port.port, baudrate=BAUDRATE, stopbits=STOPBITS,
                                       parity=PARITY, bytesize=BYTESIZE, timeout=1, xonxoff=0)
                # device.flushInput()
                # device.flushOutput()
                device.write(b"I\r")
                time.sleep(0.1)
                from_device = device.read_all().decode("utf-8")
                print(from_device)
                logging.info('from data: {0}'.format(from_device))
                if from_device == ID_MESSAGE:
                    self.found = True
                    logging.info("Found device")
                    self.connected = True
                    return device

            except Exception as exception:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print("No device at port: {0}".format(port))
                print("Exception: {0} at {1}".format(exception, exc_tb.tb_lineno))
                return None


class ThreadedUSBDataCollector(threading.Thread):
    def __init__(self, device: IoTComm, master,
                 # data_queue: queue.Queue, data_event: threading.Event,
                 function_call=None, termination_flag=False):
        threading.Thread.__init__(self)
        self.device = device
        self.master = master
        self.data_queue = data_queue
        self.data_event = data_event
        # self.func_call = function_call
        self.running = True  # bool: Flag to know when the data read should stop
        self.termination_flag = termination_flag  # Flag to know when the thread should stop

    def run(self):
        """ Poll the USB for new data packets and pass it through the queue and set the event flag so the main
        program will update the graph.  Structure the program so if the termination flag is set, collect the last
        data point to clear the data from the sensor."""

        while not self.termination_flag:
            logging.debug("In data collection thread")
            if self.running:
                data = self.device.read_all_data()
                logging.debug("Got data: {0}".format(data))
                # make sure there is data and that the previous data has been processed
                # if data and self.data_queue.empty():
                #     self.data_queue.put(data)
                #     self.data_event.set()
                if data:
                    # self.func_call(data)
                    self.master.data_processing(data)
                elif not data:
                    self.termination_flag = True
                    logging.error("=================== Device not working =====================")
            else:  # the main program wants to stop the program
                self.termination_flag = True
        logging.debug("exiting data thread call: {0}".format(self.termination_flag, hex(id(self.termination_flag))))
        # print(hex(id(self.termination_flag)))
        self.data_event.set()  # let the main program exit the data_read wait loop

    def stop_running(self):
        logging.debug("Stopping data stream")
        self.running = False


def find_available_ports():

    # taken from http://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

    if sys.platform.startswith('win'):
        _ports = ['COM%s' % (i+1) for i in range(32)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        _ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        _ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    available_ports = []
    for port in _ports:
        try:
            device = serial.Serial(port=port, write_timeout=0.5,
                                   inter_byte_timeout=1, baudrate=115200,
                                   parity=serial.PARITY_EVEN, stopbits=1)
            device.close()
            available_ports.append(device)
        except (OSError, serial.SerialException):
            pass
    return available_ports

if __name__ == '__main__':
    FORMAT = '%(levelname)s %(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    IoTComm(1, 1, 1)
    # ports = find_available_ports()
    # for port in ports:
    #     print(port.port)
    #     device = serial.Serial(port.port, baudrate=BAUDRATE, stopbits=STOPBITS,
    #                            parity=PARITY, bytesize=BYTESIZE, timeout=1)
    #     device.write(b"I\r")
    #     time.sleep(0.5)
    #     from_device = device.read_all().decode("utf-8")
    #     print('from data: ', from_device)
