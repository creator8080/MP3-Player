from multiprocessing import Value
from re import M
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit,QMessageBox,QListWidget,
 QHBoxLayout, QVBoxLayout,QFileDialog,QTextBrowser, QSlider,QListView,QComboBox)
from PyQt5.QtCore import Qt,QTimer,QStringListModel 
from PyQt5.QtGui import QPalette,QIcon, QBrush, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys
from time import *
from random import *
from PyQt5.Qt import QUrl, Qt
import ast
from PyQt5.QtGui import *
import os
from os.path import basename
from PyQt5.QtCore import *

app = QApplication([])
main = QWidget()
main.setGeometry(600,500,600,500)
main.setWindowTitle('MP3-Player')
app.setWindowIcon(QIcon('Mp3-Player-icon.png'))

m = 0
s = 0 
time_total = 0
min = 0
sec = 0
counto = 0

row = QVBoxLayout()
row1 = QHBoxLayout()
row2 = QHBoxLayout()
row3 = QHBoxLayout()
row4 = QHBoxLayout()
row5 = QHBoxLayout()
row6 = QHBoxLayout()
row7 = QHBoxLayout()

player = QMediaPlayer()
player_duration = player.duration()
volumslider = QSlider(Qt.Horizontal)
volumslider.setFocusPolicy(Qt.NoFocus)
choose = ''
volumslider.setValue(0)
volum = volumslider.value()
playlists_lst = []
def change_volume(valum):
    player.setVolume(valum)
    colum_count.setText(str(valum))
volumslider.valueChanged[int].connect(change_volume)
with open('for_player','r') as f:
    what = f.read()
lst = ast.literal_eval(what)
with open('all_playlist.txt','r') as f:
    whats = f.read()
playlists_lst = ast.literal_eval(whats)
if not str(os.path.abspath('for_player.txt')) in playlists_lst:
    with open('all_playlist.txt','w') as f:
        p = os.path.abspath('for_player.txt')
        print(p)
        playlists_lst.append(p)
        whats = f.write(str(playlists_lst))
with open('all_playlist.txt','r') as f:
    whats = f.read()
playlists_lst = ast.literal_eval(whats)
choose = basename(playlists_lst[0])
now = 0
player.setMedia(QMediaContent(QUrl('')))
item_list = lst
model = QStringListModel()
full = QListView()
model.setStringList(item_list)
full.setModel(model)
plaing = QLabel('Now playing: ')
plaing_long = QLabel('Long of music: ')
file_name = QLineEdit()
add_file_name = QPushButton('Create')
delete_file_name = QPushButton('Delete')
play = QPushButton('Play')
all_play_list = QComboBox()
for i in playlists_lst:
    all_play_list.addItems([str(basename(i))])
next = QPushButton('Next')
rands = QPushButton('Play Random')
secret = QPushButton('Hide all songs')
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
row4.addWidget(secret)
row4.addWidget(rands)
row5.addWidget(plaing)
row5.addWidget(plaing_long)
row6.addWidget(file_name)
row6.addWidget(add_file_name)
row7.addWidget(all_play_list)
row7.addWidget(delete_file_name)

def playMedia():
    if play.text() == 'Play':
        player.play()
        play.setText('Pause')
    else:
        player.pause()
        play.setText('Play')

def check_music_status():
    global m
    global s
    global player_duration
    player_status = player.mediaStatus()
    player_duration = player.duration()
    m = player_duration//1000//60
    s = player_duration//1000%60
    time_total = f'{m:>1}:{s:0>2}'
    #print(time_total)
    #print ("Текущий статус игрока", player_status)
    if player_status == 7:
        next_music()

def long_song():
    global m
    global s
    player_duration2 = player.duration()
    m = player_duration2//1000//60
    s = player_duration2//1000%60
    time_total = f'{m:>1}:{s:0>2}'
    plaing_long.setText('| Long of song: ' + f'{time_total}')

timer = QTimer()
timer.setInterval(1000)
timer.start()
timer.timeout.connect(check_music_status)
timer2 = QTimer()
timer2.setInterval(100)
timer2.start()
timer2.timeout.connect(long_song)   

def next_music():
    global now
    global lst
    if now > len(lst) - 1:
        now = 0
    #print(lst[now])
    player.setMedia(QMediaContent(QUrl(lst[now])))
    long_song()
    plaing.setText('Now playing: ' + str(basename(str(lst[now]))))
    now += 1
    playMedia()
    playMedia()

def resets():
    global lst
    global now
    player.setMedia(QMediaContent(QUrl(lst[now-1])))
    plaing.setText('Now playing: ' + str(basename(str(lst[now-1]))))
    playMedia()
    playMedia()

def backs():
    global lst
    global now
    if now == 1:
        pass
    else:
        player.setMedia(QMediaContent(QUrl(lst[now-2])))
        plaing.setText('Now playing: ' + str(basename(str(lst[now-2]))))
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
    with open(choose,'w') as f:
        f.write(str(lst))

def ran():
    global lst
    global now
    hides()
    with open(choose,'w') as f:
        shuffle(lst)
        f.write(str(lst))
    now = 0
    item_list = lst
    model.setStringList(item_list)
    full.setModel(model)
    next_music()
    hides()
    playMedia()
    playMedia()

def download():
    global lst
    wb_patch = QFileDialog.getOpenFileName()[0]
    with open(choose,'w') as f:
        lst.append(wb_patch)
        f.write(str(lst))
    item_list = lst
    model.setStringList(item_list)
    full.setModel(model)

def create():
    global all_play_list
    name_play_list = file_name.text()
    if not os.path.abspath(name_play_list + '.txt') in playlists_lst and name_play_list != '':
        file = open(name_play_list + '.txt', 'a')
        total = os.path.abspath(name_play_list + '.txt')
        file_name.setText('')
        playlists_lst.append(total)
        with open('all_playlist.txt','w') as f:
            f.write(str(playlists_lst))
        all_play_list.clear()
        for i in playlists_lst:
            all_play_list.addItems([str(basename(i))])
        file.close()
        with open(name_play_list + '.txt','w') as f:
            f.write('[]')

def stat():
    global lst
    global choose
    global model
    global full
    global now
    if secret.text() == 'Show all songs':
        secret.setText('Hide all songs') 
    now = 0
    if all_play_list.currentText() != '':
        choose = all_play_list.currentText()
        with open(choose,'r') as f:
            need = f.read()
            lst = ast.literal_eval(need)
            item_list = lst
            model.setStringList(item_list)
            full.setModel(model)

def delete():
    global choose
    global counto
    global all_play_list
    global playlists_lst
    for i in playlists_lst:
        if i != os.path.abspath('for_player.txt'):
            if i == os.path.abspath(choose):
                with open('all_playlist.txt','w') as f:
                    playlists_lst.remove(os.path.abspath(choose))
                    os.remove(os.path.abspath(choose))
                    f.write(str(playlists_lst))        
                all_play_list.removeItem(counto)
            counto += 1
        else:
            pass

def radio_play():
    player.setMedia(QMediaContent(QUrl('http://europaplus.hostingradio.ru:8014/ep-top256.mp3')))
    plaing.setText('Сейчас играет: Радио - Европа плюс')
    playMedia()
    playMedia()

def hides():
    if secret.text() == 'Hide all songs':
        item_list = []
        model.setStringList(item_list)
        full.setModel(model)
        plaing.hide()
        secret.setText('Show all songs')
    else:
        stat()
        plaing.show()
        secret.setText('Hide all songs')    

full.doubleClicked.connect(remove)
play.clicked.connect(playMedia)
back.clicked.connect(backs)
reset.clicked.connect(resets)
next.clicked.connect(next_music)
add_file_name.clicked.connect(create)
secret.clicked.connect(hides)
rands.clicked.connect(ran)
radio.clicked.connect(radio_play)
load.clicked.connect(download)
delete_file_name.clicked.connect(delete)
all_play_list.currentTextChanged.connect(stat)
row.addLayout(row1)
row.addLayout(row2)
row.addLayout(row5)
row.addLayout(row4)
row.addLayout(row3)
row.addLayout(row6)
row.addLayout(row7)
main.setLayout(row)

main.show()
app.exec_()
