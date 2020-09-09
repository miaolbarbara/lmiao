from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Graphic.ui_graphic_widget import *
from Graphic.CustomFigCanvas_essai2 import *
from Graphic.Graphic_AddSignals import *
import random
import sip
import time
from datetime import datetime,timedelta

import matplotlib as mpl
mpl.use('QT5Agg')
'''
reference:
https://www.youtube.com/watch?v=PE3yRw87T3E
https://www.thepoorengineer.com/en/arduino-python-plot/
'''

def isNumber(value):
    '''
    :param value: value is signal value decoded by database
    :return: True if it's number
             False if it's not a number
    '''
    try:
        value + 1
    except TypeError:
        return False
    else:
        return True
# ------------------------------------------------------------------------------
# Custom QTreeWidget
# ------------------------------------------------------------------------------
class DemoSignalTree(QTreeWidget):
    flag_get_DBC = 0
    flag_ListUpdated = False
    def __init__(self):
        super(DemoSignalTree,self).__init__()

        styleSheet = """
        QTreeView {
            alternate-background-color: #e8f4fc;
            background: #f6fafb;
        }
        """
        self.setStyleSheet(styleSheet)
        self.setAlternatingRowColors(True)

        self.setColumnCount(3)
        self.setHeaderLabels(['State','Color','Name'])
        self.setColumnWidth(0,5)
        self.setColumnWidth(1,5)
        # ---------create context menu----------
        self.title = "Add Signals"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300
        self.ContextMenu()
        # these following three list is used for avoidance of repetition in treeview
        self.item = []
        self.list_SignalName = []
        self.signal = {} # <- key: signal_name value: signal_color

    def get_DBC(self,DBC_path):
        # get database file from main window
        if DBC_path:
            # Graphic_AddSignals is to choose signals to be drawn
            self.Graphic_AddSignals = Graphic_AddSignals(DBC_path)
            self.Graphic_AddSignals.Signal_save_signal.connect(self._Update_signal_tree)
            self.flag_get_DBC = 1

    def _Update_signal_tree(self,list_SignalName):
        # in this signal_tree, different signals will be assigned with different colors.
        # colors are in hex
        for signal in list_SignalName:
            if signal not in self.signal:
                # give random color
                colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
                color = ''
                for i in range(6):
                    color += colorArr[random.randint(0, 14)]
                color = '#' + color
                if color not in self.signal.values():
                    item = CustomTreeItem(self, signal,color)
                    color = item.color
                    # avoidance of repetition
                    self.item.append(item)
                    self.signal[signal] = color
                self.flag_ListUpdated = True

    def return_selected_SignalName(self):
        # return dict of signal name and color
        return self.signal

    # ------Right Click Menu-------
    def ContextMenu(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        # the 'Add Signals' button is connected with action 'add signals'
        Add_signals_Act = contextMenu.addAction("Add Signals")
        Add_signals_Act.triggered.connect(self._add_signal)
        # TODO: the 'Add System Variable' button should be connected with action 'add system variable'
        Add_SV_Act = contextMenu.addAction("Add System Variables")
        # the 'Remove' button is connected with delete action
        Remove_Act = contextMenu.addAction("Remove ")
        shortcut = QShortcut(QKeySequence("Delete"), self)
        shortcut.activated.connect(self._remove_signal)
        Remove_Act.triggered.connect(self._remove_signal)
        # execute actions
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

    def _add_signal(self):
        # action: show the widget
        if self.flag_get_DBC == 1:
            self.Graphic_AddSignals.show()
        else:
            self.Graphic_AddSignals = Graphic_AddSignals(db_path= None)
            self.Graphic_AddSignals.show()
    def _remove_signal(self):
        # action: remove items
        item_to_delete = []
        for item in self.item:
            if item.checkState(0) == QtCore.Qt.Checked:
                item_to_delete.append(item)
                # Remove this item from this tree.
        for i in item_to_delete:
            sip.delete(i)
            self.item.remove(i)

    def clean_widget(self):
        # reset flags and clean widgets
        self.flag_get_DBC = 0
        self.clear()
        if self.flag_get_DBC == 1:
            self.Graphic_AddSignals._clean_clear()

# ------------------------------------------------------------------------------
# Custom QTreeWidgetItem------
# ------------------------------------------------------------------------------
class CustomTreeItem(QTreeWidgetItem):
    '''
    Custom QTreeWidgetItem with Widgets
    '''
    def __init__( self, parent, name, color_by_defalt ):
        '''
        parent (QTreeWidget) : Item's QTreeWidget parent.
        signal_name   (str)         : chosen CAN signal name
        '''
        self.color_name = color_by_defalt

        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeItem, self ).__init__( parent )

        ## Column 0 - checkbox:
        self.setCheckState(0, Qt.Unchecked)

        ## Column 1 - color-picker button:
        self.button = QPushButton()
        self.button.resize(2,2)
        self.treeWidget().setItemWidget( self, 1, self.button )
        self.button.clicked.connect(self._color_picker)
        self.button.setStyleSheet("background-color: %s " % color_by_defalt)
        ## Column 2 - Signal_name:
        self.setText(2,str(name))

    def _color_picker(self):
        print('de')
        color = QColorDialog.getColor()
        self.button.setStyleSheet("background-color: %s " % color.name())
        self.color_name = color.name()

    @property
    def name(self):
        '''
        Return qtreewidgetitem
        '''
        return self
    @property
    def color(self):
        '''
        Return signal color
        '''
        return self.color_name

# ------------------------------------------------------------------------------
# ------Custom GRAPHIC window------
# it includes two part: QTreeWidget and FigureCanvas
# ------------------------------------------------------------------------------
class CAN_Graphic(QWidget, Ui_Form):
    update_data = 'stop'
    flag_pause = False
    Timer_update = QTimer()
    SignalName_dict = None

    def __init__(self, queue,list_CAN_bus,parent=None):
        '''
        this is a main widget for GRAPHIC function
        :param queue: msg buffer
        :param list_CAN_bus: a list of buses filtered
        '''
        super(CAN_Graphic, self).__init__(parent)
        self.setupUi(self)

        self.message_queue = queue
        self.list_CAN_bus = list_CAN_bus
        # SignalView is an instance of class DemoSignalTree
        self.SignalView = DemoSignalTree()
        # instantise canvas
        self.figure = Figure()
        self.canvas = DemoFigureCanvas_essai(figure=self.figure)

        self.canvas.setStyleSheet("background-color:transparent;")
        self.canvas.show()

        self.verticalLayout = QVBoxLayout()
        self.toolbar = NavigationToolbar(self.canvas,parent)
        self.verticalLayout.addWidget(self.toolbar)
        self.verticalLayout.addWidget(self.canvas)

        self.horizontalLayout.addWidget(self.SignalView)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.setLayout(self.horizontalLayout)
        self.Timer_update.timeout.connect(self.update_data)
        # empty dictionaries, their key is SignalName
        self.instant_code = {}
        self.ani = {}

    def get_DBC(self,DBC_path):
        # get database from main window
        if DBC_path:
            self.data_time = {}
            self.data_value = {}
            self.color = {}
            self.y_ticks = {}
            self.y_ticklabels = {}
            self.db = cantools.database.load_file(DBC_path)
            self.SignalView.get_DBC(DBC_path)

    def create_lines(self):
        # once the signals are chosen and stored in the dictionary, lines of signal values in the figures will be
        # updated, the axe range will be initialised as well
        if self.SignalView.flag_ListUpdated:
            self.SignalName_dict = self.SignalView.return_selected_SignalName()
            length = len(self.SignalName_dict)
            for SignalName,color in self.SignalName_dict.items():
                self.data_time[SignalName] = []
                self.data_value[SignalName] = []
                self.color[SignalName] = color
                self.canvas.creat_lines(SignalName,self.color[SignalName],length)
            self.data_time_range = []
            self.data_value_range = []
            self.canvas.flag_get_DBC = 1
            self.SignalView.flag_ListUpdated = False

    def update_data(self):
        if self.SignalView._Update_signal_tree:
            self.create_lines()
        self.get_data_from_queue()

    def get_data_from_queue(self):
        while True:
            if self.flag_pause:
                break
            else:
                while not self.message_queue.empty():
                    # channel filter
                    msg = self.message_queue.get()
                    if msg.channel in self.list_CAN_bus:
                        if self.SignalName_dict:
                            for SignalName in self.SignalName_dict:
                                # SignalName_dict: key:selected signal names in SignalTreeView, value: color
                                try:
                                    # this following part is used to parse msg
                                    if SignalName in self.db._frame_id_to_message[msg.arbitration_id].signal_tree:
                                        if len(msg.data) < self.db._frame_id_to_message[msg.arbitration_id].length:
                                            length_diff = self.db._frame_id_to_message[msg.arbitration_id].length - len(msg.data)
                                            msg_data = list(msg.data)
                                            if str(self.db._frame_id_to_message[msg.arbitration_id].signals[0].byte_order) == 'big_endian':
                                                msg_data = list([0] * length_diff + msg_data)
                                            else:
                                                msg_data = list(msg_data + [0] * length_diff)
                                            msg.data = bytearray(msg_data)
                                        instant_decode = self.db.decode_message(msg.arbitration_id, msg.data)
                                        instant_value = instant_decode[SignalName]

                                        # if signal value is Number, no need to update y_ticks;
                                        # if signal value is a string of text, update y_ticks
                                        if isNumber(instant_value):
                                            self.y_ticks[SignalName] = None
                                            self.y_ticklabels[SignalName] = None
                                        else:
                                            self.y_ticks[SignalName], self.y_ticklabels[SignalName] = self.generate_y_ticker(self.db,msg.arbitration_id,SignalName)

                                        self.data_time[SignalName].append(msg.timestamp)
                                        self.data_value[SignalName].append(instant_value)
                                        # update axis range
                                        self.data_time_range.append(msg.timestamp)
                                        self.data_value_range.append(instant_value)

                                except KeyError:
                                    break

                            if self.data_time_range:
                                # the range of datetime is [time_min-5s,time_max+5s]
                                data_time_max = datetime.fromtimestamp(max(self.data_time_range)) + timedelta(seconds=10)
                                data_time_min = datetime.fromtimestamp(min(self.data_time_range)) - timedelta(seconds=5)

                                # in case that the msg is transferred very fast, the execution time of real time
                                # plotting is very long, we add a time.sleep here
                                time.sleep(0.2)

                                # With help of FunAnimation to update line data. In order to speed up this function,
                                # set blit as True so that only modified parts will be updated in the figure
                                for SignalName in self.data_time.keys():
                                    self.ani[SignalName] = animation.FuncAnimation(self.figure,
                                                                                    func=self.canvas.animate_data(data_time=self.data_time[SignalName],
                                                                                                                  data_value=self.data_value[SignalName],
                                                                                                                  data_time_min=data_time_min,
                                                                                                                  data_time_max=data_time_max,
                                                                                                                  y_tickers=self.y_ticks[SignalName],
                                                                                                                  y_ticklabels=self.y_ticklabels[SignalName],
                                                                                                                  SignalName=SignalName
                                                                                                                 ),
                                                                                    interval=200,
                                                                                    blit=True)
                                    self.canvas.draw()

    def clear_all(self):
        self.SignalView.clean_widget()
        self.canvas.clean_canvas()
        del self.ani

    def generate_y_ticker(self,db,msg_id,SignalName):
        '''
        :param db: *dbc
        :param msg_id: identifier in messages(MID)
        :param SignalName: SignalName decoded by database
        :return: y_ticks and y_ticklables
        '''
        y_ticks = []
        y_ticklabels = []
        name = db._frame_id_to_message[msg_id].name
        for signal in db._name_to_message[name].signals:
            if signal.name == SignalName:
                signal_choices = signal.choices
                for index in signal_choices.keys():
                    y_ticks.append(index)
                for signal_value in signal_choices.values():
                    y_ticklabels.append(signal_value)
        return y_ticks,y_ticklabels


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MyGraphicWidget = CAN_Graphic()
    MyGraphicWidget.show()
    sys.exit(app.exec_())
