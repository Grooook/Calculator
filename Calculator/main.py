from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
import math
from decimal import *


class Gui_calculator(QtWidgets.QMainWindow):
    def __init__(self, request='', main_page_show=True):
        self.curent_num = ''
        self.curent_result = ''
        self.nums = list()
        self.operations = list()
        self.history_log_text = ''
        self.log_text = ''
        self.lust_operation = ''
        super(Gui_calculator, self).__init__()
        loadUi('UI/Calc_Gui.ui', self)
        self.set_align()
        self.set_buttons()

    def set_align(self):
        self.set_state("0")
        self.log.setAlignment(QtCore.Qt.AlignRight)
        self.curent_state.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.history.setAlignment(QtCore.Qt.AlignRight)
        self.history_log.setAlignment(QtCore.Qt.AlignRight)
        self.history_log.setWordWrap(True)

    def set_buttons(self):
        # numbers
        self.pb_zero.clicked.connect(lambda: self.click_num('0'))
        self.pb_one.clicked.connect(lambda: self.click_num('1'))
        self.pb_two.clicked.connect(lambda: self.click_num('2'))
        self.pb_three.clicked.connect(lambda: self.click_num('3'))
        self.pb_four.clicked.connect(lambda: self.click_num('4'))
        self.pb_five.clicked.connect(lambda: self.click_num('5'))
        self.pb_six.clicked.connect(lambda: self.click_num('6'))
        self.pb_seven.clicked.connect(lambda: self.click_num('7'))
        self.pb_eight.clicked.connect(lambda: self.click_num('8'))
        self.pb_nine.clicked.connect(lambda: self.click_num('9'))
        self.pb_point.clicked.connect(lambda: self.click_num('.'))
        self.pb_change.clicked.connect(lambda: self.click_num('+/-'))
        # operations
        self.pb_div.clicked.connect(lambda: self.click_operation('/'))
        self.pb_mul.clicked.connect(lambda: self.click_operation('*'))
        self.pb_sub.clicked.connect(lambda: self.click_operation('-'))
        self.pb_add.clicked.connect(lambda: self.click_operation('+'))
        self.pb_mod.clicked.connect(lambda: self.click_operation('%'))
        self.pb_div_x.clicked.connect(self.one_div_x)
        self.pb_square.clicked.connect(self.num_square)
        self.pb_root.clicked.connect(self.num_root)
        self.pb_eq.clicked.connect(self.equal_result)
        self.pb_clear.clicked.connect(self.reset)
        self.pb_back.clicked.connect(self.backspace)

    def backspace(self):
        if len(self.curent_num) > 0:
            self.curent_num = self.curent_num[:-1]
            self.set_state(self.curent_num)

    def reset(self):
        self.curent_num = ''
        self.curent_result = ''
        self.nums = list()
        self.operations = list()
        self.log_text = ''
        self.lust_operation = ''
        self.set_state("0")
        self.print_log()

    def equal_result(self):
        if len(self.nums) == 1 and self.curent_num == '':
            pass
        elif len(self.nums) >= 1:
            if self.curent_num != '':
                self.click_operation(self.operations[-1])

            if len(self.nums) <= len(self.operations):
                del self.operations[-1]
                self.print_log()

            result = self.curent_result
            self.history_log_text = self.log_text + '\n=' + self.curent_result + '\n\n' + self.history_log_text
            self.history_log.setText(self.history_log_text)
            self.reset()
            self.set_state(result)

    def print_log(self):
        self.log_text = ''
        for i in range(len(self.nums)):
            try:
                self.log_text += self.nums[i] + ' '
            except:
                pass
            try:
                self.log_text += self.operations[i] + ' '
            except:
                pass
        self.log.setText(self.log_text)

    def one_div_x(self):
        self.curent_num = str(1 / Decimal(self.curent_num))
        self.set_state(self.curent_num)

    def num_square(self):
        self.curent_num = str(Decimal(self.curent_num) ** 2)
        self.set_state(self.curent_num)

    def num_root(self):
        self.curent_num = str(math.sqrt(Decimal(self.curent_num)))
        self.set_state(self.curent_num)

    def click_operation(self, operation):
        try:
            if self.lust_operation == 'num':
                self.nums.append(self.curent_num)
                self.operations.append(operation)
                error_div_zero = False
                if len(self.nums) < 2:
                    self.curent_num = ''

                elif self.nums[-1] == '0' and self.operations[-2] == '/':
                    error_div_zero = True
                    self.curent_num = ''
                    del self.nums[-1]
                    del self.operations[-1]

                else:
                    self.curent_num = ''
                    if self.operations[-2] == '-':
                        if self.curent_result == '':
                            self.curent_result = str(Decimal(self.nums[-2]) - Decimal(self.nums[-1]))
                        else:
                            self.curent_result = str(Decimal(self.curent_result) - Decimal(self.nums[-1]))

                    elif self.operations[-2] == '+':
                        if self.curent_result == '':
                            self.curent_result = str(Decimal(self.nums[-2]) + Decimal(self.nums[-1]))
                        else:
                            self.curent_result = str(Decimal(self.curent_result) + Decimal(self.nums[-1]))

                    elif self.operations[-2] == '/':
                        if self.curent_result == '':
                            self.curent_result = str(Decimal(self.nums[-2]) / Decimal(self.nums[-1]))
                        else:
                            self.curent_result = str(Decimal(self.curent_result) / Decimal(self.nums[-1]))


                    elif self.operations[-2] == '*':
                        if self.curent_result == '':
                            self.curent_result = str(Decimal(self.nums[-2]) * Decimal(self.nums[-1]))
                        else:
                            self.curent_result = str(Decimal(self.curent_result) * Decimal(self.nums[-1]))

                    elif self.operations[-2] == '%':
                        if self.curent_result == '':
                            self.curent_result = str(Decimal(self.nums[-2]) % Decimal(self.nums[-1]))
                        else:
                            self.curent_result = str(Decimal(self.curent_result) % Decimal(self.nums[-1]))

                self.print_log()
                if error_div_zero:
                    self.set_state("Error div by zero")
                else:
                    self.set_state(self.curent_result)
                self.lust_operation = 'operation'

            else:
                self.operations[-1] = operation
                self.print_log()
        except Exception as e:
            print(e)

    def set_state(self, num):
        self.curent_state.setText(num)

    def click_num(self, num):
        if num == '0' and self.curent_num == '':
            self.curent_num = '0'
        elif num == '.':
            if self.curent_num == '':
                self.curent_num = '0.'
            else:
                self.curent_num += num
        elif num == '+/-':
            if self.curent_num == '':
                self.curent_num = '-'
            elif self.curent_num[0] == '-':
                self.curent_num = self.curent_num[1:]
            else:
                self.curent_num = '-' + self.curent_num

        elif self.curent_num == '':
            self.curent_num = num
        elif self.curent_num != '0':
            self.curent_num += num

        self.lust_operation = 'num'
        self.set_state(self.curent_num)


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        widget = QtWidgets.QStackedWidget()
        widget.setWindowTitle('Calculator')
        mainwindow = Gui_calculator()
        widget.addWidget(mainwindow)
        widget.show()

    except Exception as e:
        print(e)

try:
    sys.exit(app.exec_())
except:
    print('Exiting')
