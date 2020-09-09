from __future__ import print_function, absolute_import

import can
from can.listener import Listener
from can.io.generic import BaseIOHandler
import time
import os


class CAN_bus_virtuel:
    def __init__(self, bus_channel, bus_type):
        self.bus_channel = bus_channel
        self.bus_type = bus_type


'''
module CAN_Rx initialise the bus as receptor and create two listeners for printer and logger
more details about printer and logger is in python-can
'''


class CAN_rx:
    def __init__(self):
        self.print_message()
        self.record_message()
        # self.parser_message()

    def set_bus_rx(self, bus_channel, bus_type, Queue):
        self.bus = can.interface.Bus(channel=bus_channel, bustype=bus_type)
        self.msg = Queue
        print('bus_rx is set')
        return self.bus

    def print_message(self):
        print('start to print messages')
        self.notifier = can.Notifier(self.bus, [Printer(self.msg)])
        return self.notifier

    def record_message(self, bus, BLFfile_name):
        # bus can be a bus or list
        listeners = [can.Logger(BLFfile_name)]
        self.notifier_logger = can.Notifier(bus, listeners)
        return self.notifier_logger


'''
inherit and reform printer from python-can
'''


class Printer(BaseIOHandler, Listener):
    def __init__(self, Queue, file=None):
        self.write_to_file = file is not None
        super(Printer, self).__init__(file, mode='w')
        self.queue = Queue

    def on_message_received(self, msg):
        if self.write_to_file:
            self.file.write(str(msg) + '\n')
        else:
            self.queue.put(msg)


'''
module CAN_tx is used to initialise the bus as sender.
It will send CAN messages from blf.file every 0.1 second
'''


class CAN_tx:
    def __init__(self):
        self.send_msg()

    def set_bus_tx(self, bus_channel, bus_type):
        self.bus = can.interface.Bus(channel=bus_channel, bustype=bus_type)
        print('bus_tx is set')
        return self.bus

    def send_msg(self):
        print('send msg')
        path = os.getcwd().replace("\\","/")
        filename = path+'/test_data/logging_court.blf'
        # filename = 'logging_court.blf'
        log = can.BLFReader(filename)
        log = list(log)
        for num in range(0, len(log) - 1):
            msg_arbitration_id = log[num].arbitration_id
            msg_data = log[num].data
            # msg_channel = log[num].channel
            msg = can.Message(is_extended_id=False, arbitration_id=msg_arbitration_id, data=msg_data)
            time.sleep(0.1)
            self.bus.send(msg)