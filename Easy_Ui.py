from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from Ui_UI_test3_2 import Ui_MainWindow
import time
import os
import re
from selenium.common.exceptions import WebDriverException
## 导入子窗口与父窗口
import Ui_Children_Ui,Ui_Parent_Ui,Ui_Grandson_Ui
## 导入爬虫脚本
import Easy_Exp
## 需要提取一些全局变量

Break_sign = False
## 继承两个窗口
class mywindow(QtWidgets.QMainWindow,Ui_Parent_Ui.Ui_MainWindow):
    def  __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        ## 设置下默认值免得麻烦
        self.Username_Text.setText(name)
        self.Password_Text.setText(password)
        self.Login_Button.clicked.connect(self.login_test)
        self.actionAbout.triggered.connect(self.showAuthor)
        self.actionExit.triggered.connect(self.close)

    ##定义作者信息
    def showAuthor(self):
        QMessageBox.about(self, "About", "作者：Enming Huang\n版本：1.0\nQQ：358701468\n仅用于学习交流")


    ##登陆函数 这里需要验证密码是否正确
    def login_test(self):
        global name
        global password
        name=self.Username_Text.text()
        password=self.Password_Text.text()
        print(name,password)
        if Easy_Exp.correct_password(name,password):
            Login_success()
        else:
            QMessageBox.warning(self, "Error", "密码错误或者网络问题", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            print('密码错误或者网络问题')

## chirld窗口继承
class childwindow(QtWidgets.QMainWindow,Ui_Children_Ui.Ui_MainWindow):
    def  __init__(self):
        super(childwindow, self).__init__()
        self.setupUi(self)
        self.Start_Button.clicked.connect(self.Start_loop)
        self.End_Button.clicked.connect(self.End_loop)
        ## 设置点初始值 懒狗
        self.lineEdit_ExperimentInfo.setText(Exp_info)
        self.comboBox.setCurrentText(device_name_default)
        self.lineEdit_Appointer.setText(Appoint)
        self.lineEdit_Data.setText(da_ta)
        self.lineEdit_Begin.setText(time_begin)
        self.lineEdit_End.setText(time_end)
        self.doubleSpinBox.setValue(delay_time)
        self.lineEdit_EBL1.setText(EBL_1)
        self.lineEdit_EBL2.setText(EBL_2)
        ##
        ## 这里也可以设置点默认值
    ## 开始抢实验循环
    def Start_loop(self):
        global Break_sign
        Break_sign=False
        #Begin_scripty()
        try:
            driver=Easy_Exp.open_webdriver()
        except WebDriverException: ### 打开网页超时
            QMessageBox.warning(self, "网络超时", "进不去网站", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return
        try:
            Easy_Exp.login_next(driver,name,password)
            Easy_Exp.add_exp(driver)
            ## 这里要不可以来个读文件函数设置下默认值 感觉很棒哇
            device_name=self.comboBox.currentText()
            device_id=find_device(device_name)
            ## 确认下名字对应得设备网页里面得value下标
            Exp_info=self.lineEdit_ExperimentInfo.text()
            Appoint=self.lineEdit_Appointer.text()
            da_ta=self.lineEdit_Data.text()
            time_begin=self.lineEdit_Begin.text()
            time_end=self.lineEdit_End.text()
            delay_time=self.doubleSpinBox.value()
            EBL_1=self.lineEdit_EBL1.text()
            EBL_2=self.lineEdit_EBL2.text()
            #print(EBL_1)
            #print(EBL_2)
            #print(device_id)
        except WebDriverException:
            print("浏览器莫名关闭_填信息前")
            QMessageBox.warning(self, "网络超时", "非正常关闭", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return 
        try:
            ## 填写预约信息 这里我要添加下EBL要求
            Easy_Exp.fill_info(driver,device_id,Exp_info,Appoint,da_ta,time_begin,time_end,EBL_1,EBL_2)
        except WebDriverException:
            print("浏览器莫名关闭_填信息时")
            QMessageBox.warning(self, "网络超时", "非正常关闭", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
            return 
        while True:
            ## 这里预约成功和失败分开两个try吧
            ## 成功情况
            try:
                success_class_message=driver.find_element_by_class_name('success')
                ## 这是成功预约情况
                if success_class_message:
                    print('抢到实验了')
                    QMessageBox.information(self, '恭喜','抢到实验了',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                    return
            except WebDriverException:
                print('没有预约成功')
            ## 失败情况
            try:
                #error_message=driver.find_element_by_class_name('errornote')
                #error_list=driver.find_element_by_xpath("//ul[@class='errornote']//li")
                error_list=driver.find_element_by_class_name("errorlist")
                ##
                #print('测试找到error_list没')
                #print(error_list)
                ## 如果有找到了errorlist
                if error_list:
                    s=error_list.text
                    #print(s)
                    if s=='只能预约一周内的实验，请修改.':
                        print(s)
                        Easy_Exp.crack_code(driver)
                        time.sleep(delay_time)
                        driver.find_element_by_class_name('default').click()  ##点击保存
                        continue
                    elif s=='请在工作时段预约':
                        print(s)
                        QMessageBox.information(self, '错误','请在工作时段预约',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                        return
                    elif s=='若是新增预约，该时间段已预约,请修改实验时间后保存。如果是修改已有的预约，请先取消该预约，然后新增预约':
                        print(s)
                        QMessageBox.information(self, '错误','该时间段已被预约，请换个时间',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                        return
                    elif s=='请完善用户信息后再预约实验。在首页【用户信息】后，单击【+增加】。':
                        print(s)
                        QMessageBox.information(self, '错误','请完善用户信息',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                        return
                    elif re.search('请提前12小时预约',s):
                        print(s)
                        QMessageBox.information(self, '错误','请提前12小时预约',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                        return
                    else:
                        print(s)
                        QMessageBox.information(self, '错误',s,QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
                        return
            except WebDriverException:
                print('没有错误信息，可能预约成功或者被别人抢了')
                QMessageBox.warning(self, "看看界面到哪了", "浏览器被强制退出", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                return
            
            '''
            Easy_Exp.crack_code(driver)
            time.sleep(delay_time)
            driver.find_element_by_class_name('default').click()  ##点击保存
            '''
            ################################    
            '''
                if(error_message and (not Break_sign)):
                    try:
                        Easy_Exp.crack_code(driver)
                        time.sleep(delay_time)
                        driver.find_element_by_class_name('default').click()  ##点击保存
                    except:
                            return
                    ## 这里有收到终止和找到判断
                    else:
                        #driver.quit()
                        return

                except:
                    print('info页面不存或者error没找到或者有correct')
                    return
            
        except:
            print('打不开网页')
            return
        '''
     ###############       
            '''
            try:
                submit=driver.find_element_by_class_name('default')
                WebDriverWait(driver,10,0.1).until(EC.visibility_of((submit)))
                print('info页面页面存在')
            except:
                print('info页面不存在')
                #break
                ##可以增加推出等等异常模块判断
            try:
                Easy_Exp.crack_code(driver)
                time.sleep(delay_time)
                driver.find_element_by_class_name('default').click()  ##点击保存
            except:
                break
            '''

    ## 结束抢实验
    def End_loop(self):
        global Break_sign
        Break_sign = True
        self.close()

'''
## grandson窗口继承
class grandwindow(QtWidgets.QMainWindow,Ui_Grandson_Ui.Ui_MainWindow):
    def  __init__(self):
        super(grandwindow, self).__init__()
        self.setupUi(self)
        self.quit_Button.clicked.connect(self.close)
        self.stop_Button.clicked.connect(self.stop_scripty)
    def stop_scripty(self):
        global Break_sign
        Break_sign=True
'''

## 登陆验证函数
def Login_success():
    sub.show()

'''
## 脚本运行时候的控制
def Begin_scripty():
    gan.show()
'''

## 设备id确认
def find_device(device_name_text):
    if device_name_text == '新磁控':
        return '19'
    elif device_name_text == 'EBL':
        return '6'
    elif device_name_text == 'MJB4光刻机':
        return '14'
    else:
        return '31'

## 读取默认值给全局变量
def read_file():
    f=open('default_settings.txt','r',encoding='UTF8')
    #global a
    a=[]
    for line in f.readlines()[4:]:
        line=line.strip('\n')
        point=re.search('#',line)
        #print(point)
        #point.span()返回tuple
        line=line[0:(point.span())[0]].replace(' ','')
        a.append(line)
    f.close()
    global name,password,device_name_default,Exp_info,Appoint,da_ta,time_begin,time_end,delay_time,EBL_1,EBL_2
    name=a[0]
    password=a[1]
    device_name_default=a[2]
    Exp_info=a[3]
    Appoint=a[4]
    da_ta=a[5]
    time_begin=a[6]
    time_end=a[7]
    delay_time=float(a[8])
    EBL_1=a[9]
    EBL_2=a[10]
## 标准启动模块
if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    read_file()
    ## 初始化默认参数
    sub = childwindow()
    #gan = grandwindow()
    ui = mywindow()    
    #ui.Login_Button.clicked.connect(Login)
    ui.show()
    sys.exit(app.exec_())