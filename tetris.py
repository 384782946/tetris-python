#coding=gbk
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor,QPalette
import sys
import PyQt5
from enum import Enum
import random

class MoveOrientation(Enum):
    Up=1
    Down=2
    Left=3
    Right=4

class BlockState(Enum):
    Normal = 1
    Moveable = 2
    Bottom = 3

class BlockType(Enum):
    FK = 1 #fang kuai
    TU = 2 #
    YI = 3
    LL = 4
    LR = 5
    ZL = 6
    ZR = 7
    MAX = 8
    
widgets = []
RowCount = 16
ColoumCount = 10
MinRow = RowCount

class BlockWidget(QtWidgets.QWidget):
    def __init__(self):
        super(BlockWidget,self).__init__()
        self.setAutoFillBackground(True)
        self.setState(BlockState.Normal)
    
    def setState(self,state = BlockState.Normal):
        palette = PyQt5.QtGui.QPalette()
        if state == BlockState.Moveable:
            self.color = QColor(255, 170, 0)
            palette.setColor(QPalette.Background, self.color)
        elif state == BlockState.Bottom:
            self.color = QColor(255, 170, 0)
            palette.setColor(QPalette.Background, self.color)
        else:
            self.color = QColor(120,120,120)
            palette.setColor(QPalette.Background, self.color)
        self.setPalette(palette)
        self.repaint()
        
class Index():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def getx(self):
        return self.x
        
    def gety(self):
        return self.y
    
    def setIndexState(self,state):
        if self.isValid():
            widget = widgets[self.x*ColoumCount+self.y]
            if widget:
                widget.setState(state)
    
    def prerRotate(self,center):
        ox = self.x - center.getx()
        oy = self.y - center.gety()
        return Index(center.getx()+oy,center.gety()-ox)
        
    def rotate(self,center):
        ox = self.x - center.getx()
        oy = self.y - center.gety()
        self.x = center.getx() + oy
        self.y = center.gety() - ox
             
    def preMove(self,orient):
        if orient == MoveOrientation.Up:
            return Index(self.x-1,self.y)
        elif orient == MoveOrientation.Down:
            return Index(self.x+1,self.y)
        elif orient == MoveOrientation.Left:
            return Index(self.x,self.y-1)
        elif orient == MoveOrientation.Right:
            return Index(self.x,self.y+1)
            
    def move(self,orient):
        if orient == MoveOrientation.Up:
            self.x -= 1
        elif orient == MoveOrientation.Down:
            self.x += 1
        elif orient == MoveOrientation.Left:
            self.y -= 1
        elif orient == MoveOrientation.Right:
            self.y += 1
    
    def isValid(self):
        return self.x<RowCount and self.y>=0 and self.y < ColoumCount
    
    def isSame(self,other):
        return self.x == other.getx() and self.y == other.gety()
    
class MoveableBlock():
    def __init__(self):
        self.indexs = []
        self.center = None
        self.type = random.randint(1,7)
        self.createIndex(self.type)
    
    def createIndex(self,type):
        self.indexs.clear()
        centery = int(ColoumCount/2)
        if type == 1: #int(BlockType.FK):
            self.indexs.append(Index(0,centery))
            self.indexs.append(Index(1,centery))
            self.indexs.append(Index(0,centery+1))
            self.indexs.append(Index(1,centery+1))
        elif type == 2: #int(BlockType.TU):
            self.indexs.append(Index(0,centery))
            self.indexs.append(Index(1,centery-1))
            self.center = Index(1,centery)
            self.indexs.append(self.center)
            self.indexs.append(Index(1,centery+1))
        elif type == 3: #int(BlockType.YI):
            self.center = Index(0,centery)
            self.indexs.append(self.center)
            self.indexs.append(Index(0,centery-1))
            self.indexs.append(Index(0,centery+1))
            self.indexs.append(Index(0,centery+2))
        elif type == 4: #int(BlockType.LL):
            self.center = Index(1,centery+1)
            self.indexs.append(self.center)
            self.indexs.append(Index(0,centery))
            self.indexs.append(Index(1,centery))
            self.indexs.append(Index(1,centery+2))
        elif type == 5: #int(BlockType.LR):
            self.center = Index(1,centery+1)
            self.indexs.append(self.center)
            self.indexs.append(Index(0,centery+2))
            self.indexs.append(Index(1,centery+2))
            self.indexs.append(Index(1,centery))
        elif type == 6: #int(BlockType.ZL):
            self.center = Index(1,centery)
            self.indexs.append(self.center)
            self.indexs.append(Index(0,centery))
            self.indexs.append(Index(1,centery+1))
            self.indexs.append(Index(2,centery+1))
        elif type == 7: #int(BlockType.ZR):
            self.center = Index(1,centery)
            self.indexs.append(self.center)
            self.indexs.append(Index(0,centery+1))
            self.indexs.append(Index(1,centery+1))
            self.indexs.append(Index(2,centery))
        for index in self.indexs:
            index.setIndexState(BlockState.Moveable)
        
    def getIndexs(self):
        return self.indexs
    
    def rotate(self,bottomBlock):
        if not self.center:
            return 0
        for item in self.indexs:
            retateItem = None
            if not item.isSame(self.center):
                retateItem = item.prerRotate(self.center)
                if not retateItem.isValid():
                    return 1
                elif bottomBlock.isHave(retateItem):
                    return 2
        for index in self.indexs:
            index.setIndexState(BlockState.Normal)
            index.rotate(self.center)
        for index in self.indexs:
            index.setIndexState(BlockState.Moveable)
    
    def move(self,orient,bottomBlock):
        for item in self.indexs:
            item = item.preMove(orient)
            if not item.isValid():
                return 1
            elif bottomBlock.isHave(item):
                return 2
        for index in self.indexs:
            index.setIndexState(BlockState.Normal)
            index.move(orient)
        for index in self.indexs:
            index.setIndexState(BlockState.Moveable)
        return 0
        
class BottomBlock():
    def __init__(self):
        self.indexs = []
        self.rowIndex = RowCount
        for widget in widgets:
            if widget:
                widget.setState(BlockState.Normal)
        
    def isHave(self,index):
        for item in self.indexs:
           if item.isSame(index):
               return True
        else:
            return False
        
    def rowCount(self):
        return RowCount - self.rowIndex
    
    def merge(self,indexs):
        for index in indexs:
            if index.getx() < self.rowIndex:
                self.rowIndex = index.getx()
            index.setIndexState(BlockState.Bottom)
            self.indexs.append(index)
        
    def getIndexAtRow(self,row):
        indexs = []
        for index in self.indexs:
            if index.getx() == row:
                indexs.append(index)
        return indexs
    
    def reduce(self):
        rows = []
        count = self.rowIndex-1
        for row in range(RowCount-1,count,-1):
            print("row:",row)
            indexs = self.getIndexAtRow(row)
            if len(indexs) == ColoumCount:
                rows.append(row)
                self.rowIndex += 1
                for item in indexs:
                    item.setIndexState(BlockState.Normal)
                    self.indexs.remove(item)
            else:
                for item in indexs:
                    for j in range(0,len(rows)):
                        item.setIndexState(BlockState.Normal)
                        item.move(MoveOrientation.Down)
                        item.setIndexState(BlockState.Bottom)
                
class MyDialog(QtWidgets.QDialog):
    def __init__(self):
        super(MyDialog,self).__init__()
        self.scoreView = QtWidgets.QLabel("0")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSpacing(5)
        self.rootLayout = QtWidgets.QVBoxLayout()
        self.vboxLayout = QtWidgets.QHBoxLayout()
        label=QtWidgets.QLabel("分数:")
        self.vboxLayout.addWidget(label)
        self.vboxLayout.setAlignment( QtCore.Qt.AlignRight)
        self.vboxLayout.addWidget(self.scoreView)
        self.rootLayout.addLayout(self.vboxLayout,1)
        self.rootLayout.addLayout(self.gridLayout,10)
        self.score = 0
        for i in range(0,RowCount):
            for j in range(0,ColoumCount):
                blockWidget = BlockWidget()
                widgets.append(blockWidget)
                self.gridLayout.addWidget(blockWidget,i,j)
        self.setLayout(self.rootLayout)
        self.resize(400,500)
        self.bottomBlock = None
        self.moveableBlock = None
        self.started = False
        self.timerid = -1
        
    def moveDown(self):
        ret = self.moveableBlock.move(MoveOrientation.Down,self.bottomBlock)
        if not ret == 0:
            self.bottomBlock.merge(self.moveableBlock.getIndexs())
            rowNum = self.bottomBlock.rowCount()
            self.bottomBlock.reduce()
            if self.bottomBlock.rowCount()>=RowCount:
                QtWidgets.QMessageBox.information(self, "Information", "Game Over!")
                self.killTimer(self.timerid)
                self.started = False
            else:
                self.score += 100*(rowNum - self.bottomBlock.rowCount())
                self.scoreView.setText(str(self.score))
                self.moveableBlock = MoveableBlock()
                
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            if not self.started:
                self.bottomBlock = BottomBlock()
                self.moveableBlock = MoveableBlock()
                self.timerid = self.startTimer(1000)
                self.started = True
        elif self.started:
            if event.key() == QtCore.Qt.Key_Up:
                self.moveableBlock.rotate(self.bottomBlock)
            elif event.key() == QtCore.Qt.Key_Down:
                self.moveDown()
            elif event.key() == QtCore.Qt.Key_Left:
                self.moveableBlock.move(MoveOrientation.Left,self.bottomBlock)
            elif event.key() == QtCore.Qt.Key_Right:
                self.moveableBlock.move(MoveOrientation.Right,self.bottomBlock)
        return QtWidgets.QDialog.keyPressEvent(self, event)
    
    def timerEvent(self, event):
        self.moveDown()
        return PyQt5.QtWidgets.QDialog.timerEvent(self, event)

app = QtWidgets.QApplication(sys.argv)
dlg = MyDialog()
dlg.show()
app.exec_()