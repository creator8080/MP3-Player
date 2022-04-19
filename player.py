from multiprocessing import Value
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit,QMessageBox,QListWidget,
 QHBoxLayout, QVBoxLayout,QFileDialog,QTextBrowser, QSlider,QListView)
from PyQt5.QtCore import Qt,QTimer,QStringListModel 
from PyQt5.QtGui import QPalette,QIcon, QBrush, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
from time import *
from random import *
from PyQt5.Qt import QUrl, Qt
import ast

app = QApplication([])
main = QWidget()
main.setGeometry(400,300,400,300)
main.setWindowTitle('MP3-Player')
app.setWindowIcon(QIcon('Mp3-Player-icon.png'))

row = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()
row4 = QHBoxLayout()

player = QMediaPlayer()
volumslider = QSlider(Qt.Horizontal)
volumslider.setFocusPolicy(Qt.NoFocus)
volumslider.setValue(0)
volum = volumslider.value()
def change_volume(valum):
    player.setVolume(valum)
    colum_count.setText(str(valum))
volumslider.valueChanged[int].connect(change_volume)
with open('for_player.txt','r') as f:
    what = f.read()
lst = ast.literal_eval(what)
print(lst)
now = 0
player.setMedia(QMediaContent(QUrl('')))
item_list = lst
model = QStringListModel()
full = QListView()
model.setStringList(item_list)
full.setModel(model)
play = QPushButton('Play')
next = QPushButton('Next')
rands = QPushButton('Random')
back = QPushButton('Back')
reset = QPushButton('Reset')
radio = QPushButton('Radio')
load = QPushButton('Download song')
volum_know = QLabel('Volum loud:')
colum_count = QLabel(str(volum))

row1.addWidget(play)
row1.addWidget(next)
row1.addWidget(back)
row1.addWidget(reset)
row1.addWidget(radio)
row2.addWidget(volum_know)
row2.addWidget(volumslider)
row2.addWidget(colum_count)
row3.addWidget(load)
row3.addWidget(full)
row4.addWidget(rands)

def playMedia():
    if play.text() == 'Play':
        player.play()
        play.setText('Pause')
    else:
        player.pause()
        play.setText('Play')
def next_music():
    global now
    global lst
    if now > len(lst) - 1:
        now = 0
    #print(lst[now])
    player.setMedia(QMediaContent(QUrl(lst[now])))
    now += 1
    playMedia()
    playMedia()

def resets():
    global lst
    global now
    player.setMedia(QMediaContent(QUrl(lst[now-1])))
    playMedia()
    playMedia()

def backs():
    global lst
    global now
    if now == 1:
        pass
    else:
        player.setMedia(QMediaContent(QUrl(lst[now-2])))
        now -= 1
        playMedia()
        playMedia()

def remove():
    global lst
    need = (full.currentIndex().data())
    lst.remove(need)
    item_list = lst
    model.setStringList(item_list)
    full.setModel(model)
    with open('for_player.txt','w') as f:
        f.write(str(lst))

def ran():
    global lst
    global now
    with open('for_player.txt','w') as f:
        shuffle(lst)
        f.write(str(lst))
    now = 0
    item_list = lst
    model.setStringList(item_list)
    full.setModel(model)
    next_music()
    playMedia()
    playMedia()

def download():
    global lst
    wb_patch = QFileDialog.getOpenFileName()[0]
    with open('for_player.txt','w') as f:
        lst.append(wb_patch)
        f.write(str(lst))
    item_list = lst
    model.setStringList(item_list)
    full.setModel(model)

def radio_play():
    player.setMedia(QMediaContent(QUrl('http://europaplus.hostingradio.ru:8014/ep-top256.mp3')))
    playMedia()
    playMedia()

def check_music_status():
    player_status = player.mediaStatus()
    player_duration = player.duration()
    #print ("Время музыки:", player_duration)
    #print ("Текущий статус игрока", player_status)
    if player_status == 7:
        next_music()

timer = QTimer()
timer.setInterval(1000)
timer.start()
timer.timeout.connect(check_music_status)        

full.doubleClicked.connect(remove)
play.clicked.connect(playMedia)
back.clicked.connect(backs)
reset.clicked.connect(resets)
next.clicked.connect(next_music)
rands.clicked.connect(ran)
radio.clicked.connect(radio_play)
load.clicked.connect(download)
row.addLayout(row1)
row.addLayout(row2)
row.addLayout(row4)
row.addLayout(row3)
main.setLayout(row)

main.show()
app.exec_()
