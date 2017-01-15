import urllib.request
#import urllib.parse
from tkinter import *
from tkinter import ttk, filedialog, messagebox
#from getweather import *
import os
import requests
from PIL import Image
from io import BytesIO



import re

class gui():
    def __init__(self, master,u):
        entry= StringVar()
        self.master=master
        self.number=u
        master.title('Save Instagram Photos')
        master.resizable(True, True)
        self.frames=ttk.Frame(self.master)
        self.frames.grid(pady = 5)
        self.logo=PhotoImage(file ='/home/unique/Documents/instagram.png')
        self.small_logo= self.logo.subsample(2,2)
       
        ttk.Label(self.frames, image=self.small_logo).grid(row=0,column=0)

        self.input=ttk.Entry(self.master, width=40)
        self.input.grid(row=1,column=0,sticky='w')

        self.where=ttk.Entry(self.master, width=30)

        self.where.insert(0, '/home/unique/Pictures')

        self.where.grid(row=1,column=3,sticky='w')



        self.browse=ttk.Button(self.master, text="WhereTo", command=self.browse_callback)
        self.browse.grid(row=1, column=4,columnspan = 2)


        self.button=ttk.Button(self.master, text="Save Image", command=self.send)
        self.button.grid(row=1, column=1,columnspan = 1,sticky='w')
        
    
    def browse_callback(self):
        self.path = filedialog.askdirectory(initialdir = self.where.get())
        self.where.delete(0, END)
        self.where.insert(0, self.path)


    def send(self):
        self.value=self.input.get()
        self.insta = instagram(self.value)
        self.image_url=self.insta.compare()
        self.number+=1
        self.no=str(self.number)
        self.location =self.where.get()+'/coldplayimage'+self.no+'.jpg'
        try:
            urllib.request.urlretrieve(self.image_url, self.location)
            self.success=1
        except ValueError as e:
            self.success=0
            messagebox.showerror(title = 'IOError',
                                 message = ('can\'t save the image'))
            return

        if self.success==1:
            
            self.label=ttk.Label(self.master, text='Success')
            
            self.label.config(wraplength=90, justify = LEFT, background='green',font = (8))
            self.label.grid(row=3, column=0)
            self.success = 0

class instagram():
    def __init__(self,insta_url):
    
        datas = urllib.request.urlopen(insta_url).read()
        data = datas.decode('utf-8')
        self.val=['a','b','c','d']
        self.save_image=[] 
        
        for k in range(0,4):
            self.starting_text = re.search('https://ig-s-'+self.val[k]+'-a.akamaihd.net', data)
            self.start = self.starting_text.start()
            #     self.start+=k
            #     self.start
            self.last_data= data[self.start:]
            self.ending_text = re.search('.jpg',self.last_data)

            self.end = self.ending_text.end()
            

            self.save_image.append(self.last_data[0:self.end])
    def compare(self):
        
        max_height=0
        max_width=0
        for i in range(0,4):
            self.imagedata = requests.get(self.save_image[i]).content
            self.im=Image.open(BytesIO(self.imagedata))  
            (width, height)=self.im.size
            if(width>max_width and height>max_height):
                max_width=width
                max_height=height
                real_image=self.save_image[i]
        return real_image

        

def main():
  
    root=Tk()

    grap=gui(root,0)
    root.mainloop()

if __name__=="__main__":main()
