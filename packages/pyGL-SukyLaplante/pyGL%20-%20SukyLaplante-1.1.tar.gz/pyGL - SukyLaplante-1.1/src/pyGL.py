import tkinter
from tkinter import *
import time
import keyboard


Object = []
class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
class Transform:
    def __init__(self,pos,scale):
        self.position = pos
        self.scale = scale
        self.x = pos.x
        self.y = pos.y
        self.w = scale.x
        self.h = scale.y
        self.isOnCollision = False
    def Update(self):
        self.x = self.position.x
        self.y = self.position.y
        self.w = self.scale.x
        self.h = self.scale.y
    def Translate(self, x, y):

        self.position = Vector2(self.x + x,self.y + y)



    def Scale(self,x,y):
        self.scale = Vector2(self.scale.x + x, self.scale.y + y)












class Window:
    def __init__(self,title,width,height):
        self.title = title
        self.width = width
        self.height = height
        self.window = Tk()
        self.window.geometry(str(width) + "x" + str(height))
        self.window.title(self.title)
        self.Screen = tkinter.Canvas(self.window, width=self.width, height=self.width, bg='black')
        self.Screen.pack()

        self.window.maxsize(width=self.width,height=self.height)
        self.window.minsize(width=self.width,height=self.height)
    def setMaxFPS(self, maxFPS):
        time.sleep(1/maxFPS)
    def setBackgroundColor(self,color):
        self.Screen.configure(bg=color)

    def drawRect(self,transfom,color):
        self.crect = self.Screen.create_rectangle(transfom.position.x, transfom.position.y, transfom.position.x+transfom.scale.x, transfom.position.y + transfom.scale.y,fill=color)
        Object.append(transfom)

    def clearScreen(self):
        self.Screen.delete("all")
    def fdr(self,x,y,w,h,c):
        self.drawRect(Transform(Vector2(x,y),Vector2(w,h)), c)

    def loop(self):
        self.window.update()
        Object.clear()
    def GetColliderList(self):
        return Object
    def GetKey(self,key):
        if keyboard.is_pressed(key):
            return True
    def LoadImage(self,path):
        img = PhotoImage(file=path)
        return img
    def DisplayImage(self, img,x,y):
        self.Screen.create_image(x,y,image=img)
    def DrawLine(self,pos1,pos2,clr,w,outLine):
        self.Screen.create_line(self.Screen, pos1.x, pos1.y, pos2.x, pos2.y, fill=clr, width=w, outLine=outLine)