# ui file converted in py.file
from CAN_Displayer.ui_main_window import *

# function modules:
from CAN_Displayer.CAN_settings.CAN_settings import *
from CAN_Displayer.CAN_settings.CAN_bus_Module import *
from CAN_Displayer.CAN_settings.Add_CAN_bus import *

from CAN_Displayer.Trace.treewidget import *
from CAN_Displayer.Graphic.graphic_widget import *

import os
import queue
import shutil
import threading

lock = threading.Lock()


class MainW(QMainWindow, Ui_MainWindow):
    # switch of online/offline mode
    switch_mode = 'offline'
    # flags of controls "RUN", "STOP", "CLEAR"
    flag_pause = 'stop'
    flag_run = 0
    flag_clean = 0

    # in virtual mode, threading_can0 is for Rx, threading_can1 is for Tx
    # in real implementation, both are for reception
    flag_threading_can0 = 'stop'
    flag_threading_can1 = 'stop'
    # if the bus is activated or blf.file is loaded, flag_load_msg = 1
    # if there is no msg loaded, flag_load_msg =0, button"RUN" will not be activated
    flag_load_msg = 0
    # if flag_notifier_logger = 1, listener will create log files of the messages received in blf.file.
    flag_notifier_logger_can0 = 0
    flage_notifier_logger_can1 = 0

    # intialise logging file path as None
    BLFfile_name = None
    DBC_Path = None

    # storage of threadings, diction of buses to be filered
    threaings = {'threading_CAN_0': None, 'threading_CAN_1': None}
    # in virtual mode, all messages in virtual channel will be displayed
    # three lists of chosen bus who can be accessed
    list_CAN_bus_trace = ['virtual_ch', int(0), int(1)]
    list_CAN_bus_graphic = ['virtual_ch', int(0), int(1)]
    list_bus_logger = []

    lock = threading.Lock()

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # queue: msg to be treated in TRACE; queue2: msg to be treated in GRAPHIC
        self.Queue = queue.Queue()
        self.Queue2 = queue.Queue()
        self.Signal_Def()

        # Instantiate
        # self.list_CAN_bus stores bus that can be passed
        # In virtual test, messages are transmitted from CAN 1 to CAN 0
        # In real test, we have two bus entrances.
        # Therefore, self.CAN_can0 = CAN_rx, self.CAN_can1 = CAN_rx.
        self.CAN_can0 = CAN_rx
        self.CAN_can1 = CAN_tx
        self.CAN_MsgDisplayer = CAN_MsgDisplayer(self.Queue, self.list_CAN_bus_trace)
        self.CAN_GraphicWindow = CAN_Graphic(self.Queue2, self.list_CAN_bus_graphic)

    def Signal_Def(self):

        # disable and enable control buttons
        # Once switch is changed in online mode, CAN_bus_setting buttons will be enabled and
        # load_logging_file button will be disabled. In default, CAN_bus_setting buttons are disabled
        #
        # Once switch is changed in offline mode, load_logging_file button will be enabled and
        # CAN_bus_setting buttons will be disabled. In default, load_logging_file button are enabled

        # Once online/offline mode are initialed, control button "RUN" will be enabled.
        self.CAN_bus.setEnabled(False)
        self.lineEdit_0.setEnabled(False)
        self.lineEdit_1.setEnabled(False)
        self.log.setEnabled(True)
        self.lineEdit_2.setEnabled(True)
        self.label_2.setEnabled(True)
        self.log_path.setEnabled(True)
        self.sav_data.setEnabled(True)
        self.Run_2.setEnabled(False)
        self.Run_3.setEnabled(False)

        # connect buttons with signals
        #     Add file -> _Add_DBC_file
        #     Run -> _Run
        #     Run_2 -> _Pause
        #     Run_3 -> _Clean
        #     log -> _load_logging_file
        #     mode_button -> _mode_switch
        #     log_path -> _select_log_path
        #     print_data -> _open_display_window
        #     CAN_bus ->_Ini_CAN_bus
        #     sav_data ->_save_date

        self.Addfile.clicked.connect(self._Add_DBC_file)
        self.Run.clicked.connect(self._Run)
        self.Run_2.clicked.connect(self._Pause)
        self.Run_3.clicked.connect(self._Clean)
        self.CAN_bus.clicked.connect(self._Ini_CAN_bus)
        self.log.clicked.connect(self._load_logging_file)
        self.mode_button.toggled.connect(self._get_switch_mode)
        self.log_path.clicked.connect(self._select_log_path)
        self.print_data.clicked.connect(self._open_display_window)
        self.trace_graphic.clicked.connect(self._open_graphic_window)
        self.sav_data.clicked.connect(self._save_data)
        self.add_bus_trace.clicked.connect(self._add_CAN_bus_TRACE)
        self.add_bus_save.clicked.connect(self._add_CAN_bus_SAVE)
        self.add_bus_graphic.clicked.connect(self._add_CAN_bus_GRAPHIC)

        self.Channel_setting = CAN_settings()
        self.Channel_setting.Signal_Save.connect(self._Save_CAN_Setting)
        self.Channel_setting.Signal_Reset.connect(self._Reset_CAN_Setting)

        # the following three instance are three Qdialog in order to filter CAN bus
        self.Add_CAN_bus_trace = Add_CAN_bus()
        self.Add_CAN_bus_graphic = Add_CAN_bus()
        self.Add_CAN_bus_save = Add_CAN_bus()

        self.Add_CAN_bus_trace.Signal_add_can_0.connect(self._add_can_0_TRACE)
        self.Add_CAN_bus_trace.Signal_add_can_1.connect(self._add_can_1_TRACE)
        self.Add_CAN_bus_trace.Signal_Save_bus.connect(self._Save_added_bus_TRACE)

        self.Add_CAN_bus_save.Signal_add_can_0.connect(self._add_can_0_SAVE)
        self.Add_CAN_bus_save.Signal_add_can_1.connect(self._add_can_1_SAVE)
        self.Add_CAN_bus_save.Signal_Save_bus.connect(self._Save_added_bus_SAVE)

        self.Add_CAN_bus_graphic.Signal_add_can_0.connect(self._add_can_0_GRAPHIC)
        self.Add_CAN_bus_graphic.Signal_add_can_1.connect(self._add_can_1_GRAPHIC)
        self.Add_CAN_bus_graphic.Signal_Save_bus.connect(self._Save_added_bus_GRAPHIC)

    def _get_switch_mode(self):
        '''
        This function is used to check the "switch" button state.
        :return: if it's in online mode, CAN_bus_setting buttons are enabled and load_logging_file buttons
                    are disabled.
                 if it's in offline mode, CAN_bus_setting buttons are disabled and load_logging_file buttons
                    are enabled.
        '''
        if self.mode_button.isChecked():
            self.CAN_bus.setEnabled(True)
            self.log.setEnabled(False)
            self.lineEdit_2.setEnabled(False)
            self.label_2.setEnabled(False)
            self.switch_mode = 'online'
        else:
            self.CAN_bus.setEnabled(False)
            self.lineEdit_0.setEnabled(False)
            self.lineEdit_1.setEnabled(False)
            self.log.setEnabled(True)
            self.lineEdit_2.setEnabled(True)
            self.label_2.setEnabled(True)
            self.switch_mode = 'offline'

    def _Add_DBC_file(self):
        '''
        This function is used to add database file. if the file type is not *.dbc, warning box will pop out
        :return: None
        '''
        openfile_name = QFileDialog.getOpenFileName(self, 'LOAD DBC FILE', './')
        if openfile_name[0].split('.')[-1:][0] == 'dbc':
            self.DBC_Path = openfile_name[0]
            self.lineEdit.setText(self.DBC_Path)
            self.CAN_MsgDisplayer.get_DBC(self.DBC_Path)
            self.CAN_GraphicWindow.get_DBC(self.DBC_Path)

            self.db = cantools.database.load_file(self.DBC_Path)

        else:
            QMessageBox.warning(self, 'MESSAGE', 'PLEASE LOAD CORRECT DBC FILE!', QMessageBox.Yes)

    def _Ini_CAN_bus(self):
        self.Channel_setting.show()
        self.Channel_setting.exec_()

    def _Save_CAN_Setting(self):
        '''
        configure CAN bus parameters: protocol type and baud rate.
        In virtual test, messages are transmitted from CAN 1 to CAN 0, which means, CAN 0 is Rx, CAN 1 is Tx
        '''
        BitRate_0 = int(self.Channel_setting.lineEdit_can0.text()) * 1000
        BitRate_1 = int(self.Channel_setting.lineEdit_CAN1.text()) * 1000
        bus_virtuel = CAN_bus_virtuel('virtual_ch', 'virtual')
        if self.Channel_setting.checkBox_CAN0.isChecked():
            self.bus_can0 = self.CAN_can0.set_bus_rx(self.CAN_can0, 'virtual_ch', bus_virtuel.bus_type, self.Queue)
            self.lineEdit_0.setEnabled(True)
            self.lineEdit_0.setText('CAN 0 {Baud_rate} kBaud'.format(Baud_rate=BitRate_0 / 1000))
            self.flag_threading_can0 = 'start'
            # print('Rx set')
        if self.Channel_setting.checkBox_CAN1.isChecked():
            self.bus_can1 = self.CAN_can1.set_bus_tx(self.CAN_can1, 'virtual_ch', bus_virtuel.bus_type)
            self.lineEdit_1.setEnabled(True)
            self.lineEdit_1.setText('CAN 1 {Baud_rate} kBaud'.format(Baud_rate=BitRate_1 / 1000))
            self.flag_threading_can1 = 'start'
            # print('Tx set')

        QMessageBox.information(self, 'Information', 'CAN BUS IS SET', QMessageBox.Yes)
        self.Channel_setting.close()

        '''
        The following part is added the driver socketcan, which is for real test in Raspberry. CAN 0 is Rx, CAN 1 is Tx
        In real test, there are two entrance. Therefore, self.CAN_can0 and self.CAN_can1 should be initialised as 
        class CAN_rx in the beginning. 
        '''
        # BitRate_0 = int(self.Channel_setting.lineEdit_can0.text()) * 1000
        # BitRate_1 = int(self.Channel_setting.lineEdit_CAN1.text()) * 1000
        # os.system("sudo /sbin/ip link set can0 up type can bitrate {Baud_rate}".format(Baud_rate=BitRate_0))
        # os.system("sudo /sbin/ip link set can1 up type can bitrate 500000")
        # # extend transmission buffer to 1000 bits
        # os.system("sudo ip link set can0 txqueuelen 1000")
        # os.system("sudo ip link set can1 txqueuelen 1000")

        # if self.Channel_setting.checkBox_CAN0.isChecked():
        #     self.bus_can0 = self.CAN_can0.set_bus_rx(self.CAN_can0, 'can0', 'socketcan', self.Queue)
        #     self.lineEdit_0.setEnabled(True)
        #     self.lineEdit_0.setText('CAN 0 {Baud_rate} kBaud'.format(Baud_rate=BitRate_0 / 1000))
        #     self.flag_threading_can0 = 'start'
        # #   print('Rx set')
        # if self.Channel_setting.checkBox_CAN1.isChecked():
        #     self.bus_can1 = self.CAN_can1.set_bus_tx(self.CAN_can1, 'can1', 'socketcan')
        # #   self.bus_can1 = self.CAN_can1.set_bus_tx(self.CAN_can1, 'can1', 'socketcan', self.Queue)
        #     self.lineEdit_1.setEnabled(True)
        #     self.lineEdit_1.setText('CAN 1 {Baud_rate} kBaud'.format(Baud_rate=BitRate_1 / 1000))
        #     self.flag_threading_can1 = 'start'
        # #   print('Tx set')
        #
        # QMessageBox.information(self, 'Information', 'CAN BUS IS SET', QMessageBox.Yes)
        # self.Channel_setting.close()

    def _Reset_CAN_Setting(self):
        '''
        reset CAN bus parameters: baud rate is 500
        '''
        self.Channel_setting.lineEdit_can0.setText('500')
        self.Channel_setting.lineEdit_CAN1.setText('500')

    def _Run(self):
        self.flag_run = 1
        if self.flag_threading_can0 == 'start' or self.flag_threading_can1 == 'start' or self.flag_load_msg == 1:
            # enable Pause_button(Run_2) which controls msg_recv threading
            # enable Clean_button(Run_3) which will clean displayer window
            self.Run_2.setEnabled(True)
            self.Run_3.setEnabled(True)

            # this is in offline mode. all msg in blf file will be stocked in two queue.
            # A queue for TRACE, A queue for GRAPHIC
            if self.switch_mode == 'offline':
                if self.flag_notifier_logger_can0 or self.flage_notifier_logger_can1 == 1:
                    if self.BLFfile_name is None:
                        QMessageBox.information(self, 'Information', 'PLEASE CHOOSE LOGGING PATH', QMessageBox.Yes)
                        self._select_log_path()
                    else:
                        # os copy file
                        shutil.copy(self.Logging_Path, self.Save_File_Name)
                # READ BLF file
                self.can_log = can.BLFReader(self.Logging_Path)
                for msg in self.can_log:
                    self.Queue.put(msg)
                    self.Queue2.put(msg)

            # this is in online mode. all msg in bus will be stocked in two queue.
            # A queue for TRACE, A queue for GRAPHIC
            elif self.switch_mode == 'online':
                # open logging notifier of can0 or can1
                if self.flag_notifier_logger_can0 or self.flage_notifier_logger_can1 == 1:
                    if self.BLFfile_name is None:
                        QMessageBox.information(self, 'Information', 'PLEASE CHOOSE LOGGING PATH', QMessageBox.Yes)
                        self._select_log_path()
                    else:
                        # TODO: this logger only listens can0, and save all msg of can0 in self.BLFfile_name.How to
                        #  save msg of can0 and can1 in the same blf.file.
                        self.notifier_logger = self.CAN_can0.record_message(self.CAN_can0, self.list_bus_logger,
                                                                            self.BLFfile_name)
                # Start receive thread
                self.flag_pause = 'start'
                if self.flag_threading_can0 == 'start':
                    threadCan0 = threading.Thread(target=self.CAN_Msg_Receive)
                    threadCan0.start()

                    thread_Graphic = threading.Thread(target=self.CAN_Msg_Receive_Graphic)
                    thread_Graphic.start()

                if self.flag_threading_can1 == 'start':
                    threadCan1 = threading.Thread(target=self.CAN_Msg_Tx)
                    threadCan1.start()

            self.CAN_MsgDisplayer.Timer_update.start(50)
            thread_draw = threading.Thread(target=self.CAN_GraphicWindow.update_data)
            thread_draw.start()
        else:
            QMessageBox.warning(self, 'MESSAGE', 'NO MESSAGES', QMessageBox.Yes)
            pass

    # transmission thread
    def CAN_Msg_Tx(self):
        while True:
            if self.flag_clean == 1:
                break
            else:
                self.CAN_can1.send_msg(self.CAN_can1)

    # reception thread for displaying msg in text
    def CAN_Msg_Receive(self):
        while True:
            if self.flag_pause == 'stop':
                break
            else:
                msg = self.bus_can0.recv()
                self.Queue.put(msg)

    # reception thread for displaying msg in graphic
    def CAN_Msg_Receive_Graphic(self):
        while True:
            if self.flag_pause == 'stop':
                break
            else:
                lock.acquire()
                msg = self.bus_can0.recv()
                self.Queue2.put(msg)
                lock.release()

    def _Pause(self):
        # when you click Pause button, you can't click Run button until you clear the Displayer
        self.Run.setEnabled(False)
        # set pause flag as "stop"
        self.flag_pause = 'stop'
        self.CAN_GraphicWindow.flag_pause = True
        self.CAN_MsgDisplayer.clean()

    def _Clean(self):
        if self.switch_mode == 'offline':
            # in offline mode, clean logging file too
            self.Logging_Path = None
            self.lineEdit_2.setText(self.Logging_Path)

        # in online mode, shut down can bus
        # set clean flag as true
        self.flag_clean = 1
        # # as we test in Raspi, shut down can0 and can1
        # os.system("sudo /sbin/ip link set can0 down")
        # os.system("sudo /sbin/ip link set can1 down")
        self.flag_load_msg = 0
        self.Run.setEnabled(True)

        # clean dbc
        self.DBC_Path = None
        self.lineEdit.setText(self.DBC_Path)

        # clean TRACE window and GRAPHIC window
        self.CAN_MsgDisplayer.clean()
        self.CAN_MsgDisplayer.clear_window()
        self.CAN_GraphicWindow.clear_all()

    def _load_logging_file(self):
        # this fonction is only for offline mode
        if self.switch_mode == 'offline':
            print('offline,load logging file')
            openfile_name = QFileDialog.getOpenFileName(self, 'LOAD LOGGING FILE', './')
            if openfile_name[0].split('.')[-1:][0] == 'blf':
                self.Logging_Path = openfile_name[0]
                self.lineEdit_2.setText(self.Logging_Path)

                self.flag_load_msg = 1
            else:
                QMessageBox.warning(self, 'MESSAGE', 'PLEASE LOAD CORRECT BLF FILE!', QMessageBox.Yes)
                pass
        else:
            pass

    def _select_log_path(self):
        # select the logging path. For now, this function only support logging file in form of BLF
        self.Save_File_Name = QFileDialog.getSaveFileName(self, 'PLEASE SELECT THE SAVE PATH', './')[0]
        if self.Save_File_Name.split() == []:
            QMessageBox.information(self, 'Information', 'PLEASE CHOOSE PATH AND FILE', QMessageBox.Yes)
        else:
            self.BLFfile_name = self.Save_File_Name
            self.lineEdit_3.setText(self.BLFfile_name)

    def _open_display_window(self):
        # parsed msg will be displayed line by line
        self.CAN_MsgDisplayer.show()

    def _save_data(self):
        # this function is used to stop the logging notifier
        if self.flag_run == 1:
            if self.switch_mode == 'online':
                self.notifier_logger.stop()
                QMessageBox.information(self, 'MESSAGE', 'DATA SAVED!', QMessageBox.Yes)

                if self.switch_mode == 'offline':
                    QMessageBox.information(self, 'MESSAGE', 'DATA SAVED!', QMessageBox.Yes)
            else:
                pass
        else:
            QMessageBox.information(self, 'MESSAGE', 'PLEASE RUN!', QMessageBox.Yes)

    # the following functions is to choose CAN buses(can0 can1)  who can be accessed
    # those chosen buses will be stored in two list respectively for TRACE and GRAPHIC
    def _add_CAN_bus_TRACE(self):
        self.Add_CAN_bus_trace.show()
        self.Add_CAN_bus_trace.exec_()

    def _add_can_0_TRACE(self):
        can_channel = int(0)  # <- in CANalyzer, all channel is int0 or int1
        if self.Add_CAN_bus_trace.Add_CAN_0.isChecked():
            self.list_CAN_bus_trace.append(can_channel)
        elif can_channel in self.list_CAN_bus_trace:
            self.list_CAN_bus_trace.remove(can_channel)

    def _add_can_1_TRACE(self):
        can_channel = int(1)
        if self.Add_CAN_bus_trace.Add_CAN_0.isChecked():
            self.list_CAN_bus_trace.append(can_channel)
        elif can_channel in self.list_CAN_bus_trace:
            self.list_CAN_bus_trace.remove(can_channel)

    def _Save_added_bus_TRACE(self):
        # save filtrage for all windows and exit
        if self.Add_CAN_bus_trace.Add_CAN_0.isChecked():
            self.Add_CAN_bus_graphic.Add_CAN_0.setChecked(True)
            self.Add_CAN_bus_save.Add_CAN_0.setChecked(True)
        if self.Add_CAN_bus_trace.Add_CAN_1.isChecked():
            self.Add_CAN_bus_graphic.Add_CAN_1.setChecked(True)
            self.Add_CAN_bus_save.Add_CAN_1.setChecked(True)
        self.Add_CAN_bus_trace.close()

    def _add_CAN_bus_SAVE(self):
        self.Add_CAN_bus_trace.show()
        self.Add_CAN_bus_trace.exec_()

    def _add_can_0_SAVE(self):
        self.flag_notifier_logger_can0 = 1
        if self.switch_mode == 'online':
            self.list_bus_logger.append(self.CAN_can0.bus)
        print('ffff')

    def _add_can_1_SAVE(self):
        self.flage_notifier_logger_can1 = 1
        if self.switch_mode == 'online':
            self.list_bus_logger.append(self.CAN_can1.bus)
        # <- TODO: how to save logging file in offline mode

    def _Save_added_bus_SAVE(self):
        # configure filters
        if self.Add_CAN_bus_save.Add_CAN_0.isChecked():
            self.Add_CAN_bus_graphic.Add_CAN_0.setChecked(True)
            self.Add_CAN_bus_trace.Add_CAN_0.setChecked(True)
        if self.Add_CAN_bus_save.Add_CAN_1.isChecked():
            self.Add_CAN_bus_graphic.Add_CAN_1.setChecked(True)
            self.Add_CAN_bus_trace.Add_CAN_1.setChecked(True)
        self.Add_CAN_bus_save.close()

    def _open_graphic_window(self):
        self.CAN_GraphicWindow.show()

    def _add_CAN_bus_GRAPHIC(self):
        self.Add_CAN_bus_graphic.show()
        self.Add_CAN_bus_graphic.exec_()

    def _add_can_0_GRAPHIC(self):
        can_channel = int(0)  # <- in CANalyzer, all channel is int0 or int1
        if self.Add_CAN_bus_trace.Add_CAN_0.isChecked():
            self.list_CAN_bus_graphic.append(can_channel)
        elif can_channel in self.list_CAN_bus_graphic:
            self.list_CAN_bus_graphic.remove(can_channel)

    def _add_can_1_GRAPHIC(self):
        can_channel = int(1)
        if self.Add_CAN_bus_trace.Add_CAN_0.isChecked():
            self.list_CAN_bus_graphic.append(can_channel)
        elif can_channel in self.list_CAN_bus_graphic:
            self.list_CAN_bus_graphic.remove(can_channel)

    def _Save_added_bus_GRAPHIC(self):
        ## configure filters
        if self.Add_CAN_bus_graphic.Add_CAN_0.isChecked():
            self.Add_CAN_bus_save.Add_CAN_0.setChecked(True)
            self.Add_CAN_bus_trace.Add_CAN_0.setChecked(True)
        if self.Add_CAN_bus_graphic.Add_CAN_1.isChecked():
            self.Add_CAN_bus_save.Add_CAN_1.setChecked(True)
            self.Add_CAN_bus_trace.Add_CAN_1.setChecked(True)
        self.Add_CAN_bus_graphic.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MainW()
    myapp.show()
    sys.exit(app.exec_())
