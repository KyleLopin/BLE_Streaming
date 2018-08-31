# Copyright (c) 2018 Kyle Lopin (Naresuan University) <kylel@nu.ac.th>

"""
GUI to connect to 3 Bluetooth PSoC 4 with AS7262 and AS7263 sensors connected
Convert to Kivy later
"""

# standard libraries
import logging
import tkinter as tk
# local files
# import communications as comm
import CySmart

__author__ = 'Kyle Vitautas Lopin'


class IoTColorGUI(tk.Tk):
    """
    Class to display controls and data of IoT color sensors
    """
    def __init__(self, parent=None):
        tk.Tk.__init__(self, parent)
        logging.basicConfig(format='%(asctime)s %(module)s %(lineno)d: %(levelname)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
        # print("check, {:02x}".format(7898))
        a = b'7898'
        print(a.hex())
        # self.device = comm.IoTComm(self)
        self.count = 0
        self.cy = CySmart.CySmart()
        print(self.cy)

        self.cy.start(self.cy.Flag_API_RETURN, com_port='\\.\COM8')

        cyd = self.cy.send_command(self.cy.Commands['CMD_START_SCAN'], wait_for_payload=True, wait_for_complete=False)

        print('check')
        print(cyd)

        status_string = "Hold"
        # print(self.device.found, self.device.connected)
        # if not self.device.found:
        #     status_string = "Bluetooth-USB connectivity dongle not found"
        # elif not self.device.connected:
        #     status_string = "Bluetooth-USB connectivity dongle not connected"
        # else:
        #     status_string = "Hold"

        self.status_label = tk.Label(self, text=status_string)
        self.status_label.pack(side=tk.BOTTOM)

        self.after(2000, self.update)

    def update(self):
        self.after(2000, self.update)
        cyd = self.cy.send_command(self.cy.Commands['CMD_START_SCAN'], wait_for_payload=False, wait_for_complete=False)
        print('count: ', self.count)
        self.count += 1
        print('check')
        print(cyd)
        if isinstance(cyd, bool):

            return

        if self.cy.EVT_SCAN_PROGRESS_RESULT in cyd:
            print("True")
            client = self.cy.get_scan_data(cyd)[0]
            print('name:{0}'.format(client['name']))
            print('address:', self.cy.hex_array(client['BD_Address']))
        # print('check')
        # print(self.device.device.read_all())


if __name__ == '__main__':
    app = IoTColorGUI()
    app.title("QA Monitor: Perfect Earth")
    app.geometry("900x750")
    app.mainloop()
