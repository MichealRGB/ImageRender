#!/usr/bin/python
# -*- coding: UTF-8 -*-

from Tkinter import *
import tkMessageBox
from PIL import Image,ImageTk
import cv2


app = Tk()
im = Image.open("images/113.jpg")
photo = ImageTk.PhotoImage(im)
label2 = Label(app, image = photo)

def helloButton():
    print('hello button')

Button(app, text='Hello Button', command=helloButton).pack()


def callBack(event):
    print("现在的位置是", event.x, event.y)
    cv2.circle(photo, (event.x, event.y), 3, (0, 0, 255), 2)


app.bind("<Button-1>", callBack)
label2.pack()
app.mainloop()




# class Application(Frame):
#
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.pack()
#         self.createWidgets()
#
#     def createWidgets(self):
#         self.nameInput = Entry(self)
#         self.nameInput.pack()
#         self.alertButton = Button(self, text='Hello', command=self.hello)
#         self.alertButton.pack()
#
#     def hello(self):
#         name = self.nameInput.get() or 'world'
#         tkMessageBox.showinfo('Message', 'Hello, %s' % name)
#
# app = Application()
# # 设置窗口标题:
# app.master.title('Hello World')
# # 主消息循环:
# app.mainloop()
