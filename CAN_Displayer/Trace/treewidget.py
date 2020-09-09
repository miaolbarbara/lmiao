import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qdarkstyle
import cantools
from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import threading

class CAN_MsgDisplayer(QWidget):

    Timer_update = QTimer()
    signal_flag = 0
    flag_parser = 0
    def __init__(self,queue,list_CAN_bus,parent=None):
        super(CAN_MsgDisplayer, self).__init__(parent)
        self.SetUI()
        self.Timer_update.timeout.connect(self.update_displayer)
        self.queue = queue
        self.ids = {}
        self.root = {}
        self.start_time = None
        self.key = None
        self.list_CAN_bus = list_CAN_bus


    def SetUI(self):
        self.setWindowTitle('Displayer')
        self.setGeometry(300, 300, 1000, 500)
        layout = QVBoxLayout()
        self.setLayout(layout)

        # ------QTreeWidget------
        self.tree = QTreeWidget()
        layout.addWidget(self.tree)
        self.tree.setColumnCount(8)
        self.tree.setHeaderLabels(['Count','TimeStamp','DT','Channel', 'ID','DLC', 'Data','Name'])

    def draw_can_bus_message(self,msg,sorting = False):
        # Use the CAN-Bus ID as the key in the dict
        key = msg.arbitration_id

        if msg.channel in self.list_CAN_bus:
            '''如何只显示特定的can.channel的值'''
            if msg.is_extended_id:
                key |= (1 << 32)

            new_id_added, length_changed = False, False
            if not sorting:
                # Check if it is a new message or if the length is not the same
                if key not in self.ids:
                    new_id_added = True
                    # # Set the start time when the first message has been received
                    if not self.start_time:
                        self.start_time = msg.timestamp
                elif msg.dlc != self.ids[key]['msg'].dlc:
                    length_changed = True

                if new_id_added or length_changed:
                    # create a new root for new CAN frame
                    # flag_parser is a flag to active the parser part
                    self.root[key] = QTreeWidgetItem(self.tree)
                    self.flag_parser = 1

                    # It's a new message ID or the length has changed, so add it to the dict
                    # The first is the frame counter,
                    # the second is a copy of the CAN-Bus frame
                    # and the third index is the time since the previous message
                    self.ids[key] = { 'count': 0, 'msg': msg, 'dt': 0}
                else:
                    self.flag_parser = 0
                    # Calculate the time since the last message and save the timestamp
                    self.ids[key]['dt'] = msg.timestamp - self.ids[key]['msg'].timestamp

                    # Copy the CAN-Bus frame - this is used for sorting
                    self.ids[key]['msg'] = msg

                # Increment frame counter
                self.ids[key]['count'] += 1

            # Format the CAN-Bus ID as a hex value
            arbitration_id_string = '0x{0:0{1}X}'.format(msg.arbitration_id, 8 if msg.is_extended_id else 3)
            '''type of arbitration_id_string is <class 'string'> to correct later'''

            # Generate data string
            data_string = ''
            if msg.dlc > 0:
                data_string = ' '.join('{:02X}'.format(x) for x in msg.data)

            # Now draw the CAN-Bus message on the Displayer
            self.root[key].setText(0,str(self.ids[key]['count']))
            datatime = datetime.fromtimestamp(msg.timestamp).strftime('%H:%M:%S')
            self.root[key].setText(1, str(datatime))
            self.root[key].setText(2,'{0:.6f}'.format(self.ids[key]['dt']))
            self.root[key].setText(3, str(msg.channel))
            self.root[key].setText(4,arbitration_id_string)
            self.root[key].setText(5, str(msg.dlc))
            self.root[key].setText(6, data_string)

            return self.root[key]

    def get_DBC(self,DBC_path):

        if DBC_path:
            self.db = cantools.database.load_file(DBC_path)
            self.signal_flag = 1
        else:
            self.signal_flag = 0

    def draw_parsed_message(self,root,msg,db):
        if msg.arbitration_id in list(db._frame_id_to_message):
            root.setText(7, str(db._frame_id_to_message[msg.arbitration_id].name))
            if len(msg.data) < db._frame_id_to_message[msg.arbitration_id].length:
                length_diff = db._frame_id_to_message[msg.arbitration_id].length - len(msg.data)
                msg_data = list(msg.data)
                if str(db._frame_id_to_message[msg.arbitration_id].signals[0].byte_order) == 'big_endian':
                    msg_data = list([0] * length_diff + msg_data)
                else:
                    msg_data = list(msg_data + [0] * length_diff)

                msg.data = bytearray(msg_data)
            self.instant_decode = db.decode_message(msg.arbitration_id, msg.data)
            for key in self.instant_decode.keys():
                CAN_signal = QTreeWidgetItem(root)
                CAN_signal.setText(0, str(key))
                CAN_signal.setText(1, str(self.instant_decode[key]))
                if key in db._frame_id_to_message[msg.arbitration_id].signal_tree:
                    index_signal = db._frame_id_to_message[msg.arbitration_id].signal_tree.index(key)
                    unit = db._frame_id_to_message[msg.arbitration_id].signals[index_signal].unit
                    if unit:
                        CAN_signal.setText(2,str(unit))
                root.addChild(CAN_signal)
            self.tree.addTopLevelItem(root)

    def clean(self):
        self.ids = {}
        self.start_time = None
        self.signal_flag = 0

    def clear_window(self):
        self.Timer_update.stop()
        self.tree.clear()

    def update_displayer(self):
        '''draw_can_bus_message(self,msg)
        # Initialise the ID dictionary, start timestamp, scroll and variable for pausing the viewer
        self.ids = {}
        self.paused = False
        function: clear

        # Use the CAN-Bus ID as the key in the dict
        key = msg.arbitration_id
        self.start_time = None
        self.scroll = 0
        self.draw_header()
        '''
        while not self.queue.empty():
            self.msg = self.queue.get()
            self.root[self.key] = self.draw_can_bus_message(self.msg)
            if self.signal_flag and self.flag_parser == 1:
                self.draw_parsed_message(self.root[self.key],self.msg,self.db)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    Mytreewidget = CAN_MsgDisplayer()
    Mytreewidget.show()
    sys.exit(app.exec_())
