

#  Copyright (c) 2024 StarHidden
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
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

#
#  @Project name and File name:Player_py - MainWindow.py
#
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
#
import os
import NewSlider as Nsd
import PyQt5.QtMultimedia as Media
import PyQt5.QtCore as QtCore
import PyQt5.QtWidgets as UIele
import PyQt5.QtGui as QGui
import Login
import configparser

class PlayerMainWindow(UIele.QWidget):
    def __init__(self):
        super().__init__()
        
        self.GetBaseElement()
        self.setWindowTitle('本地音乐播放器')  #设置窗口的标题
        self.setWindowIcon(QGui.QIcon("img\\ic_public_music_filled.svg"))  #设置窗口的图标
        self.ScreenAdapter()  #适配屏幕大小
        self.SetCentral()  #调整位置在正中间
        self.SetWindowMinSize()  #设置窗口最小大小
        MainLayout = self.SetLayoutFrame()
        self.setLayout(MainLayout)
        
        #播放器、播放列表等应该全局单例
        #创建播放器对象
        self.player = Media.QMediaPlayer()
        #创建播放列表对象
        self.playList = Media.QMediaPlaylist(self.player)
        # 设置列表循环播放模式为默认
        self.playList.setPlaybackMode(Media.QMediaPlaylist.Loop)
        #使用当前播放列表
        self.player.setPlaylist(self.playList)
        #维护一个歌曲文件名列表
        self.fileNameList = []
        self.LoginWindow = Login.LoginWindow()
        
        #以下是槽函数
        #播放文件更改时自动设置歌曲名，将更改应用到标签上
        self.playList.currentIndexChanged.connect(self.PlayingMediaChanged)
        self.accountButton.clicked.connect(self.OpenLoginWindow)
        self.timer = QtCore.QTimer(self)  #创建计时器
        #连接持续状态与进度条更新器
        self.player.durationChanged.connect(self.UpdateSliderDuration)
        self.player.positionChanged.connect(self.UpdateSliderPosition)
        #连接位置状态与使用时间更新器
        self.player.positionChanged.connect(self.UpdateUsedTime)
        self.timer.timeout.connect(self.UpdateRemainingTime)
        #连接进度条事件与相应的处理函数
        self.slider.sliderMoved.connect(self.SliderMoved)
        self.slider.sliderReleased.connect(self.SliderReleased)
        self.slider.customSliderClicked.connect(self.SliderClicked)
        
        self.playButton.clicked.connect(self.PlayMusic)
        self.nextButton.clicked.connect(self.PlayNext)
        self.lastButton.clicked.connect(self.PlayPrevious)
        self.modelButton.clicked.connect(self.ChangeModel)
        self.fileButton.clicked.connect(self.AddToPlaylist)  #绑定选择文件的函数
        self.LoginWindow.loginSuccess.connect(self.ReadPlayList)#读取配置文件
    
    def SetLayoutFrame(self): #UI绘制的工作放在一个函数内进行
        self.L1Layout = UIele.QVBoxLayout(self)  #第一层布局，上下分割
        
        self.L2BottonWidget = UIele.QWidget()  #第二层底部容器
        self.L2BottonWidget.setFixedHeight(self.ScreenSize.height() * 0.12)  #设置底部播放栏高度
        self.L2BottonLayout = UIele.QVBoxLayout(self.L2BottonWidget)
        
        self.L2TopWidget = UIele.QWidget()  #第二层上部容器
        self.L2TopLayout = UIele.QHBoxLayout(self.L2TopWidget)
        
        self.L2Separator = UIele.QFrame()  # 创建分界线
        self.L2Separator.setFrameShape(UIele.QFrame.HLine)  # 设置为水平线
        self.L2Separator.setFrameShadow(UIele.QFrame.Raised)  # 设置边框阴影样式
        
        #添加到L1布局器，进行嵌套
        self.L1Layout.addWidget(self.L2TopWidget)
        self.L1Layout.addWidget(self.L2Separator)
        self.L1Layout.addWidget(self.L2BottonWidget)
        
        #L2上半布局，信息窗口
        self.L3TopLeftWidget = UIele.QWidget()  #左侧边栏
        self.L3TopLeftWidget.setFixedWidth(self.ScreenSize.width() * 0.1)  #左侧边栏宽度
        self.L3TopLeftLayout = UIele.QVBoxLayout(self.L3TopLeftWidget)
        
        self.L3TopRightWidget = UIele.QWidget()  #右侧堆叠区域
        self.L3TopRightLayout = UIele.QStackedLayout(self.L3TopRightWidget)
        
        self.L3Separator = UIele.QFrame()  #左右分界线
        self.L3Separator.setFrameShape(UIele.QFrame.VLine)  #垂直线
        self.L3Separator.setFrameShadow(UIele.QFrame.Raised)
        
        #添加到L2上半布局器
        self.L2TopLayout.addWidget(self.L3TopLeftWidget)
        self.L2TopLayout.addWidget(self.L3Separator)
        self.L2TopLayout.addWidget(self.L3TopRightWidget)
        
        #L2下半布局，播放器底栏
        self.L3SliderWidget = UIele.QWidget()  #进度条容器
        self.L3SliderWidget.setFixedHeight(self.ScreenSize.height() * 0.04)
        self.L3SliderLayout = UIele.QHBoxLayout(self.L3SliderWidget)
        
        #底栏下的播放按钮
        self.L3PlayBottonWidget = UIele.QWidget()
        self.L3PlayButtonLayout = UIele.QHBoxLayout(self.L3PlayBottonWidget)
        
        #添加到L2下半布局
        self.L2BottonLayout.addWidget(self.L3SliderWidget)
        self.L2BottonLayout.addWidget(self.L3PlayBottonWidget)
        
        #创建播放列表显示器
        self.playListWidget = UIele.QListWidget()
        self.L3TopRightLayout.addWidget(self.playListWidget)
        #歌曲名标签
        self.usedTimeLable = UIele.QLabel("00:00")
        self.remainingTimeLable = UIele.QLabel("00:00")
        # 进度条
        self.slider = Nsd.NewSlider(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 0)  # 初始范围设置为0，稍后会更新
        self.slider.setValue(0)  #初始值为0
        self.slider.setEnabled(False)  # 初始时禁用
        
        self.L3SliderLayout.addWidget(self.usedTimeLable)
        self.L3SliderLayout.addWidget(self.slider)
        self.L3SliderLayout.addWidget(self.remainingTimeLable)
        
        #添加侧边栏按钮
        self.playListButton = UIele.QPushButton("播放列表")
        self.playListButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        self.playListButton.setStyleSheet("""QPushButton{border: none;}
                QPushButton:hover {border: 1px solid #000000;border-radius: 4px;}""")
        
        self.accountButton = UIele.QPushButton("账号")
        self.accountButton.setFixedSize(self.ScreenSize.width() * 0.08, self.ScreenSize.width() * 0.02)
        self.accountButton.setStyleSheet("""QPushButton{border: none;}
                QPushButton:hover {border: 1px solid #000000;border-radius: 4px;}""")
        
        #将按钮加入布局
        self.L3TopLeftLayout.addWidget(self.playListButton)
        self.L3TopLeftLayout.addStretch()
        self.L3TopLeftLayout.addWidget(self.accountButton)
        
        #标签用于显示当前播放的歌曲
        self.nameOfSongs = UIele.QLabel("歌曲名")
        self.nameOfSongs.setFixedSize(self.ScreenSize.width() * 0.2, self.ScreenSize.width() * 0.02)
        
        #以下是功能按钮
        self.playButton = UIele.QToolButton()
        self.playButton.setFixedHeight(self.ScreenSize.width() * 0.02)
        self.playButton.setFixedWidth(self.ScreenSize.width() * 0.02)
        self.playState = """
                    QToolButton{border-image: url('img/ic_public_pause_norm.svg');
                    background-position: center;
                    background-repeat: no-repeat;
                    border: none;  /* 移除边框 */
                    transition: border 0.3s ease; /* 添加过渡效果，使边框显示更平滑 */}
                    QToolButton:hover {
                    border: 2px solid #000000; /* 鼠标悬停时显示黑色边框 */
                    }"""
        self.pauseState = """
                    QToolButton{border-image: url('img/ic_public_play_norm.svg');
                    background-position: center;
                    background-repeat: no-repeat;
                    border: none;  /* 移除边框 */
                    transition: border 0.3s ease; /* 添加过渡效果，使边框显示更平滑 */}
                    QToolButton:hover {
                    border: 2px solid #000000; /* 鼠标悬停时显示黑色边框 */
                    }"""
        self.playButton.setStyleSheet(self.pauseState)
        
        self.nextButton = UIele.QPushButton()
        self.nextButton.setFixedHeight(self.ScreenSize.width() * 0.02)
        self.nextButton.setFixedWidth(self.ScreenSize.width() * 0.02)
        self.nextButton.setStyleSheet("""
                    QPushButton{border-image: url('img/ic_public_play_next.svg');
                    background-position: center;
                    background-repeat: no-repeat;
                    border: none;  /* 移除边框 */transition: border 0.3s ease; /* 添加过渡效果，使边框显示更平滑 */}
                    QPushButton:hover {
                    border: 2px solid #000000; /* 鼠标悬停时显示黑色边框 */
                    }""")
        
        self.lastButton = UIele.QPushButton()
        self.lastButton.setFixedHeight(self.ScreenSize.width() * 0.02)
        self.lastButton.setFixedWidth(self.ScreenSize.width() * 0.02)
        self.lastButton.setStyleSheet("""
                    QPushButton{border-image: url('img/ic_public_play_last.svg');
                    background-position: center;
                    background-repeat: no-repeat;
                    border: none;  /* 移除边框 */
                    transition: border 0.3s ease; /* 添加过渡效果，使边框显示更平滑 */}
                    QPushButton:hover {
                    border: 2px solid #000000; /* 鼠标悬停时显示黑色边框 */
                    }""")
        
        self.modelButton = UIele.QToolButton()
        self.modelButton.setFixedHeight(self.ScreenSize.width() * 0.02)
        self.modelButton.setFixedWidth(self.ScreenSize.width() * 0.02)
        self.listCycleState = """QToolButton{border-image: url('img/ic_public_list_cycle.svg');
                    background-position: center;
                    background-repeat: no-repeat;
                    border: none;  /* 移除边框 */
                    transition: border 0.3s ease; /* 添加过渡效果，使边框显示更平滑 */}
                    QToolButton:hover {
                    border: 2px solid #000000; /* 鼠标悬停时显示黑色边框 */
                    }"""
        self.singleState = """QToolButton{border-image: url('img/ic_public_single_cycle.svg');
                    background-position: center;
                    background-repeat: no-repeat;
                    border: none;  /* 移除边框 */
                    transition: border 0.3s ease; /* 添加过渡效果，使边框显示更平滑 */}
                    QToolButton:hover {
                    border: 2px solid #000000; /* 鼠标悬停时显示黑色边框 */
                    }"""
        self.randomState = """QToolButton{border-image: url('img/ic_public_random.svg');
                    background-position: center;
                    background-repeat: no-repeat;
                    border: none;  /* 移除边框 */
                    transition: border 0.3s ease; /* 添加过渡效果，使边框显示更平滑 */}
                    QToolButton:hover {
                    border: 2px solid #000000; /* 鼠标悬停时显示黑色边框 */
                    }"""
        self.modelButton.setStyleSheet(self.listCycleState)
        
        self.fileButton = UIele.QToolButton()
        self.fileButton.setFixedHeight(self.ScreenSize.width() * 0.02)
        self.fileButton.setFixedWidth(self.ScreenSize.width() * 0.02)
        self.fileButton.setStyleSheet("""
                    QToolButton{border-image: url('img/ic_public_view_list.svg');
                    background-position: center;
                    background-repeat: no-repeat;
                    border: none;  /* 移除边框 */
                    transition: border 0.3s ease; /* 添加过渡效果，使边框显示更平滑 */}
                    QToolButton:hover {
                    border: 2px solid #000000; /* 鼠标悬停时显示黑色边框 */
                    }  """)
        
        self.L3PlayButtonLayout.addWidget(self.nameOfSongs)
        self.L3PlayButtonLayout.addStretch(1)
        self.L3PlayButtonLayout.addWidget(self.lastButton)
        self.L3PlayButtonLayout.addWidget(self.playButton)
        self.L3PlayButtonLayout.addWidget(self.nextButton)
        self.L3PlayButtonLayout.addWidget(self.modelButton)
        self.L3PlayButtonLayout.addStretch(4)
        self.L3PlayButtonLayout.addWidget(self.fileButton)
        
        return self.L1Layout
    
    def AddToPlaylist(self):
        # 弹出文件资源管理器窗口选择音乐文件
        fileName, _ = UIele.QFileDialog.getOpenFileName(self, 'Open Music File', '',
                'Music Files (*.mp3 *.wav *.ogg *.flac *.aac)')
        if fileName:
            # 将选择的文件添加到播放列表
            content = Media.QMediaContent(QtCore.QUrl.fromLocalFile(fileName))
            self.playList.addMedia(content)
            fileNameOnly = os.path.splitext(os.path.basename(fileName))[0]
            self.playListWidget.addItem(fileNameOnly)  # 在播放列表控件中添加文件名
            self.fileNameList.append(fileNameOnly)  # 将文件名称加入文件名列表
            if self.LoginWindow.ConfigFileName:#如果当前处于登录状态
                order = len(self.fileNameList) + 1  #歌曲的序号
                self.WritePlayList(fileName, order)

    
    def WritePlayList(self, fileName:str, order):
        config = configparser.ConfigParser()
        songOrder = f"song{order}"
        configFileName = self.LoginWindow.ConfigFileName
        config.read(configFileName, encoding = "GBK")
        config.set(self.LoginWindow.sectionName, songOrder, fileName)
        with open(configFileName, 'w', encoding = "GBK") as configFile:
            config.write(configFile)
    
    def ReadPlayList(self):#登录成功自动添加播放列表
        #先清空当前播放列表
        self.player.pause()#暂停播放
        self.playButton.setStyleSheet(self.pauseState)
        self.playListWidget.clear()
        self.fileNameList.clear()
        if self.playList.clear():
            config = configparser.ConfigParser()
            configFileName = self.LoginWindow.ConfigFileName
            config.read(configFileName, encoding = "GBK")  #读取配置文件
            for section in config.sections():
                if config.options(section):
                    for option in config.options(section):
                        fileName = config.get(section, option)
                        if fileName:
                            content = Media.QMediaContent(QtCore.QUrl.fromLocalFile(fileName))
                            self.playList.addMedia(content)
                            fileNameOnly = os.path.splitext(os.path.basename(fileName))[0]
                            self.playListWidget.addItem(fileNameOnly)  # 在播放列表控件中添加文件名
                            self.fileNameList.append(fileNameOnly)  # 将文件名称加入文件名列表
        else:
            print("error")
    
    def OpenLoginWindow(self):
        self.LoginWindow.show()
    
    def PlayMusic(self):
        if not self.playList.isEmpty():
            if not self.player.state() == Media.QMediaPlayer.PlayingState:
                if not self.timer.isActive():
                    self.timer.start(1000)
                self.player.play()
                self.slider.setEnabled(True)
                self.playButton.setStyleSheet(self.playState)
                self.nameOfSongs.setText(self.fileNameList[self.playList.currentIndex()])
            else:
                self.player.pause()
                self.playButton.setStyleSheet(self.pauseState)
    
    def PlayingMediaChanged(self, index):
        if not self.playList.isEmpty():
            self.nameOfSongs.setText(self.fileNameList[self.playList.currentIndex()])
        else:
            self.nameOfSongs.setText("歌曲名")
    
    def SetPosition(self, position):
        self.player.setPosition(position)
    
    def UpdateSliderPosition(self, duration):
        self.slider.setValue(duration)
    
    def UpdateSliderDuration(self, duration):
        self.slider.setRange(0, self.player.duration())
    
    def UpdateUsedTime(self, position):
        mins, secs = divmod(position // 1000, 60)
        mins = round(mins)
        secs = round(secs)
        self.usedTimeLable.setText('{:02d}:{:02d}'.format(mins, secs))
    
    def UpdateRemainingTime(self):
        if self.player.state() == Media.QMediaPlayer.PlayingState:
            remainingTime = self.player.duration() - self.player.position()
            mins, secs = divmod(remainingTime // 1000, 60)
            mins = round(mins)
            secs = round(secs)
            self.remainingTimeLable.setText('{:02d}:{:02d}'.format(mins, secs))
    
    def ChangeModel(self):
        if self.playList.playbackMode() == Media.QMediaPlaylist.Loop:
            # 设置单曲循环
            self.playList.setPlaybackMode(Media.QMediaPlaylist.CurrentItemInLoop)
            self.modelButton.setStyleSheet(self.singleState)
        else:
            if self.playList.playbackMode() == Media.QMediaPlaylist.CurrentItemInLoop:
                # 设置随机播放
                self.playList.setPlaybackMode(Media.QMediaPlaylist.Random)
                self.modelButton.setStyleSheet(self.randomState)
            else:
                self.playList.setPlaybackMode(Media.QMediaPlaylist.Loop)
                self.modelButton.setStyleSheet(self.listCycleState)
    
    def PlayNext(self):
        if not self.playList.isEmpty():
            self.playList.next()
            self.nameOfSongs.setText(self.fileNameList[self.playList.currentIndex()])
            if not self.timer.isActive():
                self.timer.start(1000)
            if self.player.state() != Media.QMediaPlayer.PlayingState:
                self.player.play()
    
    def PlayPrevious(self):
        if not self.playList.isEmpty():
            self.playList.previous()
            self.nameOfSongs.setText(self.fileNameList[self.playList.currentIndex()])
            if not self.timer.isActive():
                self.timer.start(1000)
            if self.player.state() != Media.QMediaPlayer.PlayingState:
                self.player.play()
    
    def SliderMoved(self):
        self.timer.stop()
        self.player.setPosition(round(self.slider.value() * self.player.duration() / self.player.duration()))
    
    def SliderReleased(self):
        self.timer.start()
    
    def SliderClicked(self):
        self.player.setPosition(round(self.slider.value() * self.player.duration() / self.player.duration()))
    
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
    
    def ScreenAdapter(self):
        width = self.ScreenSize.width() * 0.6  # 窗口宽度为屏幕宽度的80%
        height = self.ScreenSize.height() * 0.6  # 窗口高度为屏幕高度的60%
        self.setGeometry(100, 100, width, height)  # 设置窗口位置和大小
    
    def SetWindowMinSize(self):
        width = self.ScreenSize.width() * 0.2
        height = self.ScreenSize.height() * 0.3
        self.setMinimumSize(width, height)
