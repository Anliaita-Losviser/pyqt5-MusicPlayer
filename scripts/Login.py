
#  Copyright (c) 华南理工大学学生创新团队 Last Update: 2024-05-23 21:33:27. All Rights Reserved.
#
#  @Project name and File name:Player_py - Login.py
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#  Redistributions of source code must retain the above copyright notice,
#  this list of conditions and the following disclaimer.
#  Redistributions in binary form must reproduce the above copyright
#  notice, this list of conditions and the following disclaimer in the
#  documentation and/or other materials provided with the distribution.
#  Neither the name of the developer nor the names of its
#  contributors may be used to endorse or promote products derived from
#  this software without specific prior written permission.
#  重新分发和使用源代码和二进制形式的代码，无论是否进行修改，都是允许的，只要满足以下条件：
#  重新分发源代码时，必须保留上述版权通知、本条件列表以及以下免责声明。
#  以二进制形式重新分发时，必须在分发时提供的文档或其他材料中复制上述版权通知、本条件列表以及以下免责声明。
#  未经事先书面许可，不得使用开发者或贡献者的名称来认可或推广从本软件派生出来的产品。
#
#  Disclaimer
#  This software is provided "as is" without any express or implied warranty,
#  including but not limited to the warranties of merchantability,
#  fitness for a particular purpose, and non-infringement.
#  The risk of using this software lies with the user. The developers or contributors shall not be liable for any direct,
#  indirect, incidental, special, exemplary, or consequential damages resulting from the use of this software.
#  To the maximum extent permitted by law, the developers or contributors shall not be responsible for any claims,
#  losses, liabilities, damages, costs, or expenses arising from the use or inability to use this software.
#  免责声明
#  本软件按“现状”提供，不附带任何形式的明示或暗示保证，包括但不限于对适销性、特定用途的适用性或非侵权性的保证。
#  使用本软件的风险由用户自行承担。开发者或贡献者不对因使用本软件而导致的任何直接、间接、偶然、特殊、惩戒性或后果性损害承担任何责任。
#  在法律允许的最大范围内，开发者或贡献者对于因使用或无法使用本软件而产生的任何索赔、损失、责任、损害、成本或费用均不承担责任。

# coding = UTF-8

import ctypes
import re
import time
import random
import PyQt5.QtWidgets as UIele
import configparser
import AccountDatabase
from PyQt5.QtCore import pyqtSignal, QThread

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("Login")


class ValidateThread(QThread):
    generateCode = pyqtSignal(str)
    def __init__(self):
        super().__init__()
    
    def run(self):
        while True:
            random_number = self.generate_random_number()
            self.generateCode.emit(random_number)
            time.sleep(60)  # 等待60秒
    
    def generate_random_number(self):
        return str(random.randint(100000, 999999))
class LoginWindow(UIele.QWidget):
    loginSuccess = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.GetBaseElement()
        self.setWindowTitle('登录')
        self.SetWindowSize()  #设置窗口最小大小
        self.SetCentral()  #调整位置在正中间
        self.InitStackedFrame()
        self.StackedFrame.setCurrentIndex(0)
        self.ConfigFileName = ""
        self.sectionName = "songsList"
        self.validateCode = "000000"
        self.ValidateCoddeGenerator = ValidateThread()
        
        self.siginButton.clicked.connect(self.SwitchToSigin)
        self.backButton.clicked.connect(self.SwitchToLogin)
        self.loginButton.clicked.connect(self.Login)
        self.confirmSigninButton.clicked.connect(self.Sigin)
        self.resetPasswordButton.clicked.connect(self.SwitchToResetPassword)
        self.notResetButton.clicked.connect(self.SwitchToLogin)
        self.confirmToResetButton.clicked.connect(self.ConfirmToReset)
        self.getValidateCodeButton.clicked.connect(self.GetValidateCode)
        
        self.ValidateCoddeGenerator.generateCode.connect(self.ValidateCodeChange)
        self.ValidateCoddeGenerator.start()
        
    
    def InitStackedFrame(self):
        self.InitLoginFrame()
        self.InitSiginFrame()
        self.InitResetPasswordFrame()
        self.StackedFrame = UIele.QStackedLayout(self)
        self.StackedFrame.addWidget(self.loginWidget)
        self.StackedFrame.addWidget(self.siginWidget)
        self.StackedFrame.addWidget(self.resetpasswordWidget)
    
    def InitLoginFrame(self):
        self.loginWidget = UIele.QWidget()
        self.LoginLayout = UIele.QVBoxLayout(self.loginWidget)
        
        self.LoginTitleWidget = UIele.QWidget()
        self.LoginTitleLayout = UIele.QHBoxLayout(self.LoginTitleWidget)
        
        self.LoginEditWidget = UIele.QWidget()
        self.LoginEditLayout = UIele.QGridLayout(self.LoginEditWidget)
        
        self.LoginButtonsWidget = UIele.QWidget()
        self.LoginButtonsLayout = UIele.QHBoxLayout(self.LoginButtonsWidget)
        
        self.LoginLayout.addWidget(self.LoginTitleWidget)
        self.LoginLayout.addWidget(self.LoginEditWidget)
        self.LoginLayout.addWidget(self.LoginButtonsWidget)
        
        self.loginLabel = UIele.QLabel("登录")
        self.LoginTitleLayout.addStretch()
        self.LoginTitleLayout.addWidget(self.loginLabel)
        self.LoginTitleLayout.addStretch()
        
        self.accountLabel = UIele.QLabel("请输入账号：")
        self.LoginEditLayout.addWidget(self.accountLabel, 0, 0)
        self.accountEdit = UIele.QLineEdit(self)
        self.accountEdit.setPlaceholderText("请输入12位账号数字")
        self.LoginEditLayout.addWidget(self.accountEdit, 0, 1)
        
        self.passwordLabel = UIele.QLabel("请输入密码：")
        self.LoginEditLayout.addWidget(self.passwordLabel, 1, 0)
        self.passwordEdit = UIele.QLineEdit(self)
        self.passwordEdit.setPlaceholderText("请输入8-16位有效密码")
        self.passwordEdit.setEchoMode(UIele.QLineEdit.Password)
        self.LoginEditLayout.addWidget(self.passwordEdit, 1, 1)
        
        self.siginButton = UIele.QPushButton("注册新账号")
        self.siginButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        self.loginButton = UIele.QPushButton("登录")
        self.loginButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        self.resetPasswordButton = UIele.QPushButton("忘记密码")
        self.resetPasswordButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        
        self.LoginButtonsLayout.addWidget(self.siginButton)
        self.LoginButtonsLayout.addWidget(self.loginButton)
        self.LoginButtonsLayout.addWidget(self.resetPasswordButton)
    
    def InitSiginFrame(self):
        self.siginWidget = UIele.QWidget()
        self.SiginLayout = UIele.QVBoxLayout(self.siginWidget)
        
        self.SiginTitleWidget = UIele.QWidget()
        self.SiginTitleLayout = UIele.QHBoxLayout(self.SiginTitleWidget)
        
        self.SiginEditWidget = UIele.QWidget()
        self.SiginEditLayout = UIele.QGridLayout(self.SiginEditWidget)
        
        self.SiginButtonWidget = UIele.QWidget()
        self.SiginButtonLayout = UIele.QHBoxLayout(self.SiginButtonWidget)
        
        self.SiginLayout.addWidget(self.SiginTitleWidget)
        self.SiginLayout.addWidget(self.SiginEditWidget)
        self.SiginLayout.addWidget(self.SiginButtonWidget)
        
        self.siginLabel = UIele.QLabel("新用户注册")
        self.SiginTitleLayout.addStretch()
        self.SiginTitleLayout.addWidget(self.siginLabel)
        self.SiginTitleLayout.addStretch()
        
        self.siginAccountLabel = UIele.QLabel("请输入账号：")
        self.SiginEditLayout.addWidget(self.siginAccountLabel, 0, 0)
        self.siginAccountEdit = UIele.QLineEdit(self)
        self.siginAccountEdit.setPlaceholderText("请输入12位账号数字")
        self.SiginEditLayout.addWidget(self.siginAccountEdit, 0, 1)
        
        self.siginPasswordLabel = UIele.QLabel("请输入密码：")
        self.SiginEditLayout.addWidget(self.siginPasswordLabel, 1, 0)
        self.siginPasswordEdit = UIele.QLineEdit(self)
        self.siginPasswordEdit.setPlaceholderText("输入8-16位密码，必须包含数字、字母")
        self.siginPasswordEdit.setEchoMode(UIele.QLineEdit.Password)
        self.SiginEditLayout.addWidget(self.siginPasswordEdit, 1, 1)
        
        self.passwordConfirmLabel = UIele.QLabel("请确认密码：")
        self.SiginEditLayout.addWidget(self.passwordConfirmLabel, 2, 0)
        self.passwordConfirmEdit = UIele.QLineEdit(self)
        self.passwordConfirmEdit.setPlaceholderText("请再次输入密码")
        self.passwordConfirmEdit.setEchoMode(UIele.QLineEdit.Password)
        self.SiginEditLayout.addWidget(self.passwordConfirmEdit, 2, 1)
        
        self.confirmSigninButton = UIele.QPushButton("点击注册")
        self.confirmSigninButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        self.backButton = UIele.QPushButton("取消注册")
        self.backButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        
        self.SiginButtonLayout.addWidget(self.confirmSigninButton)
        self.SiginButtonLayout.addWidget(self.backButton)
    
    def InitResetPasswordFrame(self):
        self.resetpasswordWidget = UIele.QWidget()
        self.resetpasswordLayout = UIele.QVBoxLayout(self.resetpasswordWidget)
        
        self.resetpasswordTitleWidget = UIele.QWidget()
        self.resetpasswordTitleLayout = UIele.QHBoxLayout(self.resetpasswordTitleWidget)
        
        self.resetpasswordEditWidget = UIele.QWidget()
        self.resetpasswordEditLayout = UIele.QGridLayout(self.resetpasswordEditWidget)
        
        self.resetpasswordButtonWidget = UIele.QWidget()
        self.resetpasswordButtonLayout = UIele.QHBoxLayout(self.resetpasswordButtonWidget)
        
        self.resetpasswordLayout.addWidget(self.resetpasswordTitleWidget)
        self.resetpasswordLayout.addWidget(self.resetpasswordEditWidget)
        self.resetpasswordLayout.addWidget(self.resetpasswordButtonWidget)
        
        self.resetpasswordLabel = UIele.QLabel("重置密码")
        self.resetpasswordTitleLayout.addStretch()
        self.resetpasswordTitleLayout.addWidget(self.resetpasswordLabel)
        self.resetpasswordTitleLayout.addStretch()
        
        self.resetpasswordAccountLabel = UIele.QLabel("请输入账号：")
        self.resetpasswordEditLayout.addWidget(self.resetpasswordAccountLabel, 0, 0)
        self.resetpasswordAccountEdit = UIele.QLineEdit(self)
        self.resetpasswordAccountEdit.setPlaceholderText("请输入12位账号数字")
        self.resetpasswordEditLayout.addWidget(self.resetpasswordAccountEdit, 0, 1)
        
        self.pintoResetpasswordLabel = UIele.QLabel("请输入新密码：")
        self.resetpasswordEditLayout.addWidget(self.pintoResetpasswordLabel, 1, 0)
        self.resetpasswordEdit = UIele.QLineEdit(self)
        self.resetpasswordEdit.setPlaceholderText("输入8-16位密码，必须包含数字、字母")
        self.resetpasswordEdit.setEchoMode(UIele.QLineEdit.Password)
        self.resetpasswordEditLayout.addWidget(self.resetpasswordEdit, 1, 1)
        
        self.resetpasswordConfirmLabel = UIele.QLabel("请确认新密码：")
        self.resetpasswordEditLayout.addWidget(self.resetpasswordConfirmLabel, 2, 0)
        self.resetpasswordConfirmEdit = UIele.QLineEdit(self)
        self.resetpasswordConfirmEdit.setPlaceholderText("请再次输入密码")
        self.resetpasswordConfirmEdit.setEchoMode(UIele.QLineEdit.Password)
        self.resetpasswordEditLayout.addWidget(self.resetpasswordConfirmEdit, 2, 1)
        
        self.ValidateCodeLabel = UIele.QLabel("请输入验证码：")
        self.resetpasswordEditLayout.addWidget(self.ValidateCodeLabel, 3, 0)
        self.ValidateCodeEdit = UIele.QLineEdit(self)
        self.ValidateCodeEdit.setPlaceholderText("请输入6位验证码")
        self.resetpasswordEditLayout.addWidget(self.ValidateCodeEdit, 3, 1)
        
        self.confirmToResetButton = UIele.QPushButton("确认重置")
        self.confirmToResetButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        self.getValidateCodeButton = UIele.QPushButton("获取验证码")
        self.getValidateCodeButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        self.notResetButton = UIele.QPushButton("取消重置")
        self.notResetButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        
        self.resetpasswordButtonLayout.addWidget(self.getValidateCodeButton)
        self.resetpasswordButtonLayout.addWidget(self.confirmToResetButton)
        self.resetpasswordButtonLayout.addWidget(self.notResetButton)
    
    def SwitchToSigin(self):  #切换到注册页面
        self.StackedFrame.setCurrentIndex(1)
    
    def SwitchToLogin(self):  #返回到登录页面
        self.StackedFrame.setCurrentIndex(0)
    
    def SwitchToResetPassword(self): #切换到忘记密码
        self.StackedFrame.setCurrentIndex(2)
    def CheckAccount(self, account):  #检查账号格式
        if re.match(r'^\d{12}$', account):
            return True
        else:
            return False
    
    def CheckPassword(self, password):  #检查密码格式
        pattern = r"^(?=.*\d)(?=.*[a-zA-Z]).{8,16}$"
        if re.match(pattern, password):
            return True
        else:
            return False
    
    def Login(self):  #点击登录
        account = self.accountEdit.text()
        password = self.passwordEdit.text()
        if self.CheckAccount(account) and self.CheckPassword(password):
            self.selectDatabaseThread = AccountDatabase.SelectDatabase(account, password)
            self.selectDatabaseThread.start()
            while not AccountDatabase.IntentHelper.selectFinished:
                pass#等待查询完成
            if AccountDatabase.IntentHelper.IDCorrect:
                if AccountDatabase.IntentHelper.passwordCorrect:
                    self.GetConfigFileName(AccountDatabase.IntentHelper.configFileName)
                    time.sleep(0.2)
                    self.loginSuccess.emit("Login Successfully")
                    AccountDatabase.IntentHelper.Reset()
                    self.close()
                else:
                    message = UIele.QMessageBox()
                    message.warning(self, '警告', '输入密码不正确')
            else:
                message = UIele.QMessageBox()
                message.warning(self, '警告', '未查询到账号')
        else:
            message = UIele.QMessageBox()
            message.warning(self, '警告', '输入账号或密码格式不正确')
            self.accountEdit.clear()
            self.passwordEdit.clear()
        AccountDatabase.IntentHelper.Reset()
    
    def Sigin(self):  #点击注册
        account = self.siginAccountEdit.text()
        password = self.siginPasswordEdit.text()
        confirmPassword = self.passwordConfirmEdit.text()
        if self.CheckAccount(account) and self.CheckPassword(password) and (password == confirmPassword):
            configFileName = self.InitConfigFile(account)
            self.insertDatabaseThread = AccountDatabase.InsertDatabase(account, password, configFileName)
            self.insertDatabaseThread.start()
            while not AccountDatabase.IntentHelper.selectFinished:
                pass#等待查询
            if AccountDatabase.IntentHelper.InsertSuccess and AccountDatabase.IntentHelper.IDCorrect:
                message = UIele.QMessageBox()
                message.information(self, "提示","注册成功")
                AccountDatabase.IntentHelper.Reset()
                self.siginAccountEdit.clear()
                self.siginPasswordEdit.clear()
                self.passwordConfirmEdit.clear()
            else:
                if not AccountDatabase.IntentHelper.IDCorrect:
                    message = UIele.QMessageBox()
                    message.warning(self, '警告','注册失败，账号已存在')
                else:
                    message = UIele.QMessageBox()
                    message.warning(self, '警告', '注册失败')
                AccountDatabase.IntentHelper.Reset()
        else:
            message = UIele.QMessageBox()
            message.warning(self, '警告', '输入账号或密码格式不正确')
            self.siginAccountEdit.clear()
            self.siginPasswordEdit.clear()
            self.passwordConfirmEdit.clear()
        AccountDatabase.IntentHelper.Reset()
    
    def ConfirmToReset(self):#点击重置密码
        account = self.resetpasswordAccountEdit.text()
        newPassword = self.resetpasswordEdit.text()
        confirmNewPassword = self.resetpasswordConfirmEdit.text()
        validateCode = self.ValidateCodeEdit.text()
        if self.CheckAccount(account) and self.CheckPassword(newPassword) and (newPassword==confirmNewPassword):
            if validateCode == self.validateCode:
                self.UpdateDatabaseThread = AccountDatabase.UpadateDatabase(account, newPassword)
                self.UpdateDatabaseThread.start()
                while not AccountDatabase.IntentHelper.selectFinished:
                    pass  #等待更新
                if AccountDatabase.IntentHelper.IDCorrect:
                    message = UIele.QMessageBox()
                    message.information(self, "提示","重置成功")
                    AccountDatabase.IntentHelper.Reset()
                    self.SwitchToLogin()
                else:
                    message = UIele.QMessageBox()
                    message.warning(self, '警告', '重置失败')
                    AccountDatabase.IntentHelper.Reset()
                    self.ValidateCodeEdit.clear()
                AccountDatabase.IntentHelper.Reset()
            else:
                message = UIele.QMessageBox()
                message.warning(self, '警告', '验证码不正确')
                self.ValidateCodeEdit.clear()
        else:
            message = UIele.QMessageBox()
            message.warning(self, '警告', '输入账号或密码格式不正确')
            self.siginAccountEdit.clear()
            self.siginPasswordEdit.clear()
            self.passwordConfirmEdit.clear()
        AccountDatabase.IntentHelper.Reset()
    
    def GetValidateCode(self):
        message = UIele.QMessageBox()
        message.information(self,'验证码', self.validateCode)
    
    def ValidateCodeChange(self, code):
        self.validateCode = code
    
    def GetConfigFileName(self, filename):
        self.ConfigFileName = filename
    
    def InitConfigFile(self, account):
        config = configparser.ConfigParser()
        config[self.sectionName] = {}
        with open(f"configfiles/{account}.ini", 'w', encoding = "GBK") as configfile:
            config.write(configfile)
        filename = f"configfiles/{account}.ini"
        return filename
    
    def GetBaseElement(self):
        self.ScreenObject = UIele.QApplication.primaryScreen()
        self.ScreenSize = self.ScreenObject.size()
    
    def SetCentral(self):
        w = self.width()
        h = self.height()
        x = (self.ScreenSize.width() - w) / 2
        y = (self.ScreenSize.height() - h) / 2
        # 移动窗口到计算出的位置
        self.move(x, y)
    
    def SetWindowSize(self):
        width = self.ScreenSize.width() * 0.3
        height = self.ScreenSize.height() * 0.3
        self.setMinimumSize(width, height)
        self.setMaximumSize(width, height)