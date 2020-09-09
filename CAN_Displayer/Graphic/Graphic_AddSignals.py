import sys
import os.path
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.Qt import Qt
import cantools

class Graphic_AddSignals(QWidget):
    signal_name = []
    Signal_save_signal = QtCore.pyqtSignal(list)

    def __init__(self,db_path,parent=None):
        super(Graphic_AddSignals, self).__init__(parent)
        self.db_path = db_path
        self.SetUI()

    def SetUI(self):
        self.setWindowTitle('symbol selection')
        self.setGeometry(300, 300, 1000, 500)
        self.FixedHeight = 30

        # ------WidgetLayout------
        self.tree = QTreeWidget()
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(['Name','Tx Frame','Channel Mask','Start Bit', 'Comment'])
        self.tree.setColumnWidth(0,300)

        # set strip stylesheet
        styleSheet = """
        QTreeView {
            alternate-background-color: #e8f4fc;
            background: #f6fafb;
        }
        """
        self.setStyleSheet(styleSheet)
        self.tree.setAlternatingRowColors(True)
        # get checked items
        self.tree.itemChanged.connect(self.handleItemChanged)
        if self.db_path:
            self.db = cantools.database.load_file(self.db_path)
            self.root = QTreeWidgetItem(self.tree)
            self.root.setText(0, str(os.path.basename(self.db_path)))
            self.signals = QTreeWidgetItem(self.root)
            self.signals.setText(0, 'Signals')
            self.frames = QTreeWidgetItem(self.root)
            self.frames.setText(0, 'frames')
            self.nodes = QTreeWidgetItem(self.root)
            self.nodes.setText(0, 'nodes')

            for message in self.db.messages:
                for index, signal in enumerate(message.signals):
                    self.CAN_signal = QTreeWidgetItem(self.signals)
                    self.CAN_signal.setText(0, str(signal.name))
                    self.CAN_signal.setCheckState(0, Qt.Unchecked)
                    self.CAN_signal.setText(1, str(message.name))
                    self.CAN_signal.setText(3, str(signal.start))
                    self.signals.addChild(self.CAN_signal)

            for node in self.db.nodes:
                self.CAN_node = QTreeWidgetItem(self.nodes)
                self.CAN_node.setText(0, str(node.name))
                self.nodes.addChild(self.CAN_node)

            self.tree.addTopLevelItem(self.root)

        # ------search line------- TODO: the searching bar is not compelet. Reform the "searching bar" in the bottom
        self.custom_edit = CustomEdit(self, size=(10, 10, 120, 24),
                name='custom_edit', search=True)
        self.custom_edit.setPlaceholderText('I''m searching bar')
        data_list = [i * ('%s' % i) for i in range(15)]
        self.custom_edit.fill_data(data_list)

        # ------Text Edit-------
        self.text = QTextEdit()
        self.text.setText('choose a signal')
        self.text.setFixedHeight(self.FixedHeight*3)

        # ------SAVE and CLOSE button-------
        self.save_signal = QPushButton('SAVE')
        self.close_subwindow = QPushButton('CLOSE')
        self.save_signal.setFixedHeight(self.FixedHeight)
        self.close_subwindow.setFixedHeight(self.FixedHeight)
        self.save_signal.clicked.connect(self._Save_Signal)
        self.close_subwindow.clicked.connect(self._Close)

        self.Button = QHBoxLayout()
        self.Button.addWidget(self.save_signal)
        self.Button.addWidget(self.close_subwindow)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.custom_edit)
        self.layout.addWidget(self.tree)
        self.layout.addWidget(self.text)

        self.layout_total = QVBoxLayout()
        self.layout_total.addLayout(self.layout)
        self.layout_total.addLayout(self.Button)

        self.setLayout(self.layout_total)

    def handleItemChanged(self, item, column):
        # if a treeitem is chosen, add the item name into the list 'signal name'
        # if a treeitem is dechosen, remove the item name from the list 'signal name'
        # all the chosen item will be displayed in the text container
        if item.checkState(column) == QtCore.Qt.Checked:
            self.signal_name.append(str(item.text(0)))
            self.text.setText('\r'.join(self.signal_name[i] for i in range(len(self.signal_name))))
        elif item.checkState(column) == QtCore.Qt.Unchecked:
            if str(item.text(0)) in self.signal_name:
                self.signal_name.remove(str(item.text(0)))
                self.text.setText('\r'.join(self.signal_name[i] for i in range(len(self.signal_name))))

    def _Save_Signal(self):
        self.Signal_save_signal.emit(self.signal_name)

    def _clean_clear(self):
        self.signal_name = []
        self.db_path = None
        self.tree.clear()

    def _Close(self):
        self.close()


# TODO: searching bar
'''
searching bar
'''
class CustomEdit(QLineEdit):
    """
    search bar which is inherited from QLineEdit
    """
    def __init__(self, parent, size=(50, 50, 100, 20), name='edit',
                 drag=False, text_list=True, search=True, qss_file=''):

        super(CustomEdit, self).__init__(None, parent)
        self.w = size[2]
        self.h = size[3]
        self.setGeometry(*size)
        self.setObjectName(name)
        # if dropping event is supported
        self.drag_flag = False
        if drag:
            self.setAcceptDrops(True)
            self.setDragEnabled(True)  # 开启可拖放事件
        else:
            self.setAcceptDrops(False)
            self.setDragEnabled(False)  # 关闭可拖放事件

        self.click_flag = False  # 点击状态，为False时显示下拉框
        self.text_list = None  # 下拉框对象
        self.p_text = ""    # placehold text，输入框背景上的灰色文字
        self.qss_file = qss_file  # 下拉框样式文件
        self.org_data = []  # 用来进行搜索的数据list

        # 如果text_list为True，则初始化下拉框
        if text_list:
            # 下拉列表模型为StringListModel
            self.list_model = QtCore.QStringListModel()
            # 初始化下拉列表对象为QListView类型
            self.text_list = QListView(parent)
            # 下拉列表名称，以list_开头
            self.text_list.setObjectName("list_%s" % name)
            # 设置下拉列表初始化尺寸
            self.text_list.setGeometry(size[0], size[1]+size[3], size[2], size[3])
            # 隐藏下拉列表
            self.text_list.hide()
            # 初始化下拉列表数据
            # 点击下拉框列表元素，绑定消息响应函数
            self.func = None
            self.text_list.clicked.connect(lambda: self.on_select_data(self.func))

        if search:
            self.textChanged.connect(self.on_search_data)

    def on_select_data(self, func):
        """
        选择下拉框数据时的消息响应函数
        """
        text = ''
        idx = self.text_list.currentIndex()
        if self.text_list.data:
            text = self.text_list.data[idx.row()]
        self.text_list.hide()
        self.setText(text)
        self.setFocus()
        self.setCursorPosition(len(text))
        # 选择数据后就隐藏了下拉框，设置点击标识位为False，下次点击才会显示下拉框
        self.click_flag = False
        if func:
            func()

    def on_search_data(self):
        """
        文本变化时的消息响应，搜索下拉框列表里的数据
        """
        # 输入框中文本和List选择文本不一样的时候，才显示下拉框
        cur_text = self.text()
        list_text = ''
        idx = self.text_list.currentIndex()
        if self.text_list.data:
            list_text = self.text_list.data[idx.row()]
        if cur_text != list_text:  # and len(cur_text) > 1:
            self.text_list.show()

        # 根据消息响应传入的data来搜索
        self.text_list.data = self.org_data[:]
        for _text in self.org_data:
            if cur_text not in _text:
                self.text_list.data.remove(_text)
        # 刷新下拉框
        self.list_model.setStringList(self.text_list.data)
        self.text_list.setModel(self.list_model)

        if not self.click_flag:
            self.text_list.hide()
            self.click_flag = True
        if self.text_list.data:  # 有数据的时候就调整下拉框大小
            self.resize_text_list()
        else:
            self.text_list.hide()  # 没有数据就隐藏下拉框


    def fill_data(self, text_data_list):
        """
        初始化文本下拉输入框控件数据
        :param text_data_list: 下拉框数据，必须为纯文本list
        """
        # 设置下拉列表数据
        self.list_model.setStringList(text_data_list)
        self.text_list.setModel(self.list_model)
        self.text_list.data = text_data_list
        # 填充list数据
        if text_data_list:
            self.text_list.data = text_data_list
            self.org_data = text_data_list[:]  # 深拷贝一份数据，用来搜索
            self.text_list.resize(self.w, self.h * 0.6 * int(len(self.text_list.data)))
            self.setText(text_data_list[0])
        else:
            self.setText('')
        self.text_list.hide()

    edit_clicked = QtCore.pyqtSignal()  # 定义clicked信号

    def mouseReleaseEvent(self, event):
        """
        鼠标按键松开时的事件处理
        :param event: 鼠标按键松开事件
        """
        # 左键松开
        if event.button() == QtCore.Qt.LeftButton:
            # 下拉列表存在数据，并且未点击过，则显示下拉框
            if self.text_list.data and not self.click_flag:
                self.text_list.show()
            # 下拉列表存在，并且点击过，则隐藏下拉框
            elif self.click_flag:
                self.text_list.hide()
            self.click_flag = not self.click_flag
            self.edit_clicked.emit()  # 发送clicked信号


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Graphic_AddSignals()
    ui.show()
    sys.exit(app.exec_())