import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtCore import Qt


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.interval = 1
        self.numPlayers = 3
        self.players = ["어무니", "큰아들", "작은아들"]
        self.diffLimit = 5 * 60
        self.baseLimit = 5 * 60
        self.baseTime = 1 * 60
        self.curBaseTime = 0

        self.paused = True
        self.timer = QTimer(self)
        self.timer.setInterval(self.interval * 1000)
        self.timer.timeout.connect(self.timeout)

        self.setWindowTitle('QTimer')
        self.setGeometry(100, 100, 2000, 1200)

        layout = QVBoxLayout()

        self.lcds = []
        nameLayout = QHBoxLayout()
        lcdLayout = QHBoxLayout()
        for i, name in enumerate(self.players):
            label = QLabel(name)
            label.setAlignment(Qt.AlignCenter)
            font = label.font()
            font.setPointSize(50)
            label.setFont(font)
            nameLayout.addWidget(label)
            lcd = makeLCD()
            self.lcds.append(lcd)
            lcdLayout.addWidget(lcd)
            #
            # if i != len(self.players) - 1:
            #     nameLayout.addStretch(1)
            #     lcdLayout.addStretch(1)

        layout.addLayout(nameLayout)
        layout.addLayout(lcdLayout)

        # layout.addStretch(1)

        monitorLayout = QHBoxLayout()
        self.playerMonitor = QLabel("", self)
        self.playerMonitor.setAlignment(Qt.AlignCenter)
        self.playerMonitor.setStyleSheet("Color : Blue")
        font = self.playerMonitor.font()
        font.setPointSize(200)
        self.playerMonitor.setFont(font)
        # self.playerMonitor.setFixedHeight(400)
        # self.playerMonitor.setFixedWidth(800)
        monitorLayout.addWidget(self.playerMonitor)
        self.baseTimeMonitor = makeLCD()
        monitorLayout.addWidget(self.baseTimeMonitor)
        self.minDiffMonitor = makeLCD()
        monitorLayout.addWidget(self.minDiffMonitor)
        layout.addLayout(monitorLayout)

        btnLayout = QHBoxLayout()
        self.btnReset = QPushButton("Reset")
        self.btnReset.clicked.connect(self.onResetButtonClicked)
        self.btnReset.setFixedSize(200, 200)
        btnLayout.addWidget(self.btnReset)
        btnLayout.addStretch(1)
        self.btnStartPause = QPushButton("Start/Pause")
        self.btnStartPause.clicked.connect(self.onStartPauseButtonClicked)
        self.btnStartPause.setFixedSize(200, 200)
        btnLayout.addWidget(self.btnStartPause)
        btnLayout.addStretch(1)
        self.btnNext = QPushButton("Next")
        self.btnNext.clicked.connect(self.onNextButtonClicked)
        self.btnNext.setFixedSize(800, 200)

        btnLayout.addWidget(self.btnNext)
        layout.addLayout(btnLayout)

        layout.setStretchFactor(nameLayout, 1)
        layout.setStretchFactor(lcdLayout, 3)
        layout.setStretchFactor(monitorLayout, 5)
        layout.setStretchFactor(btnLayout, 1)
        self.onResetButtonClicked()
        self.setLayout(layout)

    def onResetButtonClicked(self):
        self.paused = True
        self.timer.stop()
        self.curIdx = 0
        self.spentTimes = [0] * self.numPlayers
        self.curBaseTime = self.baseTime
        self.refresh()

    def onStartPauseButtonClicked(self):
        if self.paused:
            self.paused = False
            self.timer.start()
        else:
            self.paused = True
            self.timer.stop()

    def onNextButtonClicked(self):
        self.curIdx = (self.curIdx + 1) % 3
        self.curBaseTime = self.baseTime
        # self.refresh()

    def timeout(self):
        sender = self.sender()
        if id(sender) == id(self.timer):
            if self.curBaseTime > 0:
                self.curBaseTime -= 1
            else:
                self.spentTimes[self.curIdx] += self.interval
            self.refresh()

    def refresh(self):
        curTime = self.spentTimes[self.curIdx]
        # minDiffTime = curTime - min(self.spentTimes)
        # remainTime = self.diffLimit - minDiffTime
        remainTime = self.baseLimit - curTime

        self.playerMonitor.setText(self.players[self.curIdx])
        self.lcds[self.curIdx].display(secondToString(curTime))
        if remainTime <= 0:
            self.minDiffMonitor.setStyleSheet("Color : red")
        elif remainTime <= 1 * 60:
            self.minDiffMonitor.setStyleSheet("Color : orange")
        else:
            self.minDiffMonitor.setStyleSheet("Color : green")
        self.minDiffMonitor.display(secondToString(remainTime))

        if self.curBaseTime > 5:
            self.baseTimeMonitor.setStyleSheet("Color : green")
        else:
            self.baseTimeMonitor.setStyleSheet("Color : orange")
        self.baseTimeMonitor.display(secondToString(self.curBaseTime))


def secondToString(seconds):
    seconds = abs(int(seconds))
    hh = seconds // 60 // 60
    mm = seconds // 60 % 60
    ss = seconds % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d}"


def makeLCD():
    lcd = QLCDNumber()
    lcd.display(secondToString(0))
    lcd.setDigitCount(8)
    return lcd


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
