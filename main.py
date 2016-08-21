import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from threading import Timer
import wx
import json
import time

class main(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Beat the Box!',size=(500,150))
        self.frame=wx.Panel(self)
        self.update()
        self.choices = ["Sticky Note Controlled", "Hand Controlled", "Face Controlled", "Eye Controlled"]
        self.seconds = ["10", "20", "30", "40", "50", "60"]
        self.boxValue = ["OFF", "ON"]
        self.dropdown=wx.ComboBox(self.frame,choices=self.choices,pos=(10,10),style=wx.CB_READONLY)
        wx.StaticText(self.frame, -1, "Time:", pos=(310, 57))
        wx.StaticText(self.frame, -1, "Box Movement:", pos=(310, 90))
        self.times=wx.ComboBox(self.frame,choices=self.seconds,pos=(350,55),style=wx.CB_READONLY)
        self.boxes=wx.ComboBox(self.frame,choices=self.boxValue,pos=(410,88),style=wx.CB_READONLY)
        go = wx.Button(self.frame,label='START',pos=(200,2),size=(250,30))
        self.Bind(wx.EVT_BUTTON, self.letsgo, go)
        self.Bind(wx.EVT_COMBOBOX, self.get_stuff,self.dropdown)
        self.t3 = wx.TextCtrl(self.frame,pos=(5, 50),size = (300,75),style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.t3.SetValue("The most beginner of all the control methods. All you do is use the yellow sticky note to beat all the boxes! Very consistent and fun! High Score: "+str(self.new_json['Sticky Note Controlled'])+" BPM")
        self.high = self.new_json
    def get_stuff(self, event):
        if self.dropdown.GetValue()=="Hand Controlled":
            self.t3.SetValue("A challenging way to beat the boxes. This way, you must have your hand in a fist and face it towards the webcam. Aim to hit the boxes! If you need more of a challenge turn on box movement! High Score: "+str(self.new_json['Hand Controlled'])+" BPM")
        elif self.dropdown.GetValue()=="Sticky Note Controlled":
            self.t3.SetValue("The most beginner of all the control methods. All you do is use the yellow sticky note to beat all the boxes! Very consistent and fun! High Score: "+str(self.new_json['Sticky Note Controlled'])+" BPM")
        elif self.dropdown.GetValue()=="Face Controlled":
            self.t3.SetValue("Ready for a the most strange way to play the game? Play it with your face! High Score: "+str(self.new_json['Face Controlled'])+" BPM")
        elif self.dropdown.GetValue()=="Eye Controlled":
            self.t3.SetValue("Another strange but fun way to beat the boxes. Play it with your eyes! Settings are toned down compared to the Sticky Note Controlled mode. High Score: "+str(self.new_json['Eye Controlled'])+" BPM")
    def update(self):
        with open('high_score.txt') as abc:
            self.new_json=json.load(abc)
    
    def letsgo(self,event):
        self.vid1 = cv.VideoCapture(0)
        self.vid1.set(3,320);
        self.vid1.set(4,240);
        self.hand_cascade = cv.CascadeClassifier('hand.xml')
        self.face_cascade = cv.CascadeClassifier('face.xml')
        self.eye_cascade = cv.CascadeClassifier('eye.xml')
        self.videoprocessor(self.dropdown.GetValue(), self.times.GetValue(), self.boxes.GetValue())
    def videoprocessor(self, typeOfInteraction, times, speedReady):
        self.new_Random(typeOfInteraction)
        found = False;
        x,y,w,h =(0,0,0,0)
        total = 0
        self.translated = typeOfInteraction
        target = time.time()+int(times)
        while True:


            _, img1 = self.vid1.read()
            if speedReady == "ON":
                self.move_me()
            cv.rectangle(img1, (self.startx, self.starty), (self.left, self.right),(0,255,0), 2)
            if self.translated == "Sticky Note Controlled":
                
                oranges = cv.cvtColor(img1, cv.COLOR_BGR2HSV)
                ORANGE_MIN = np.array([25, 25, 150],np.uint8)
                ORANGE_MAX = np.array([50, 100, 210],np.uint8)
                frame_threshed = cv.inRange(oranges, ORANGE_MIN, ORANGE_MAX)
                kernel = np.ones((9,9),np.uint8)
                erosion = cv.erode(frame_threshed,kernel,iterations = 1)
                dilation = cv.dilate(frame_threshed,kernel,iterations = 1)
                contours, hierarchy = cv.findContours(dilation,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
                for i in contours:
                    if cv.contourArea(i) > 2500:
                        x,y,w,h = cv.boundingRect(i)
                        cv.rectangle(img1,(x,y),(x+w,y+h),(0,255,0),2)
                        
            elif self.translated == "Face Controlled":
                gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.2, 3)
                
            
                for (x,y,w,h) in faces:
                    cv.rectangle(img1,(x,y),(x+w,y+h),(255,0,0),2)
                    x = x
                    y = y
                    w = w
                    h = h
            elif self.translated == "Hand Controlled":
                gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
                faces = self.hand_cascade.detectMultiScale(gray, 1.1, 4)
                
            
                for (x,y,w,h) in faces:
                    cv.rectangle(img1,(x,y),(x+w,y+h),(255,0,0),2)
                    x = x
                    y = y
                    w = w
                    h = h
            elif self.translated == "Eye Controlled":
                gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
                faces = self.eye_cascade.detectMultiScale(gray, 1.3, 4)
                whatX = []
                whatY = []
                for x,y,w,h in faces:
                    whatX.append(x)
                    whatY.append(y)
                if len(faces)!=0:

                    whatXX = min(whatX)
                    whatXY = min(whatY)
                    x = whatXX
                    y = whatXY
                    h = whatXY+100
                    w = whatXX+100
                    cv.rectangle(img1,(whatXX,whatXY),(whatXX+100,whatXY+100),(255,0,0),2)
            found = True
            color = (255,255,255)
            if self.startx < x or self.left>(x+w):
                found = False
            if self.starty < y or self.right>y+h:
                found = False
            if found == True:
                color = (0, 255, 0)
                total += 5
                self.new_Random(self.translated)
            if target - time.time()<0:
                break
            cv.putText(img1,str(total)+" : "+str(target-time.time()),(150,200), cv.FONT_HERSHEY_SIMPLEX, 1,color,2)

            cv.imshow("image",img1)
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        multi = 60/int(times)
        if (total*multi) > self.new_json[self.translated]:
            self.high.update({self.translated:total})
            print self.high
            json.dump(self.high,open('high_score.txt','w'))
        self.vid1.release()
        cv.destroyAllWindows()
        wx.MessageBox('Congrats! You earned '+str(total)+' points!!!', str(total)+ ' points!!', wx.OK | wx.ICON_INFORMATION)


    def new_Random(self, typeOfInteraction):
        self.speed = randint(1, 6)
        self.way = randint(0,1)
        if typeOfInteraction == "Hand Controlled":
            high = 250
            low = 50
        elif typeOfInteraction == "Eye Controlled" or typeOfInteraction == "Face Controlled":
           
            high = 260
            low = 50
        else:
            high = 300
            low = 30
        self.startx = randint(low, high)
        self.starty = randint(low, high-80)
        self.distance = randint(5, 30)
        self.left = self.startx+self.distance
        self.right = self.starty+self.distance
        if self.left > 320:
            self.left = 280
        if self.right > 240:
            self.right = 200

    def move_me(self):
        
        if self.way:
        
            self.startx -=self.speed
            self.left -= self.speed
        
        elif not self.way:
        
            self.startx +=self.speed
            self.left += self.speed
        
        if self.left > 320 or self.left <0:
            self.new_Random(self.translated)


if __name__ =='__main__':
    app = wx.App(False)
    window = main(parent=None,id=-1)
    window.Show()
    app.MainLoop()

"""
                for (x,y,w,h) in faces:
                    cv.rectangle(img1,(x,y),(x+w,y+h),(255,0,0),2)
                    x = x
                    y = y
                    w = w
                    h = h
"""
