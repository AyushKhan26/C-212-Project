import socket
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

import pygame
from pygame import mixer

import os
import time

import ftplib
from ftplib import FTP
import ntpath
from pathlib import Path

IP_ADDRESS =  '127.0.0.1'
PORT = 5500
SERVER = None
BUFFER_SIZE = 4096

song_counter = 0

listBox = None
selectLabel = None


def play():
  global listBox
  global song_selected
  global selectLabel

  song_selected = listBox.get(ANCHOR)

  pygame
  mixer.init()
  mixer.music.load('shared_files/'+song_selected)
  mixer.music.play()
  if(song_selected != ""):
     selectLabel.configure(text="Now Playing:"+ song_selected)
  else:
     selectLabel.configure(text=" ")

def stop():
  global song_selected
  global selectLabel

  pygame
  mixer.init()
  mixer.music.load('shared_files/'+ song_selected)
  mixer.music.pause()
  selectLabel.configure(text=" ")

def upload_song():
   global song_counter
   global listBox

   for file in os.listdir('shared_files'):
      fileName = os.fsdecode(file)
      listBox.insert(song_counter,fileName)
      song_counter = song_counter + 1

def resume():
   global song_selected
   mixer.init()
   mixer.music.load('shared_files/'+song_selected)
   mixer.music.play()

def pause():
   global song_selected
   pygame
   mixer.init()
   mixer.music.load('shared_files/'+ song_selected)
   mixer.music.pause()


def musicWindow():
    global listBox
    global selectLabel

    window = Tk()
    window.title('MUSIC WINDOW')
    window.geometry('500x500')
    window.configure(bg='LightSkyBlue')

    selectLabel = Label(window,text="SELECT SONG",bg="LightSkyBlue",font=('Calibri',10))
    selectLabel.place(x=5,y=10)

    listBox = Listbox(window,height=10,width=40,activestyle="dotbox", bg="LightSkyBlue", font=('Calibri',10))
    listBox.place(x=100,y=10)

    scrollbar1 = Scrollbar(listBox)
    scrollbar1.place(relheight=1, relx=1)
    scrollbar1.config(command= listBox.yview)

    playButton = Button(window,text="Play",width=10,bg="yellow",bd=1,font=('Helvetica',10),command=play)
    playButton.place(x=30,y=200)

    Stop = Button(window,text="Stop",bd=1,width=10,bg='yellow',font=('Helvetica',10),command=stop)
    Stop.place(x=200,y=200)

    upload = Button(window,text="Upload",bd=1,width=10,bg='cyan',font=('Helvetica',10),fg="white",command=upload_song)
    upload.place(x=30,y=250)

    download = Button(window,text="Download",width=10,bd=1,bg="cyan",font=('Calibri',10))
    download.place(x=200,y=250)

    resume_button = Button(window,text="Resume",width=10,bd=1,bg='cyan',font=('Calibri',10),command=resume)
    resume_button.place(x=30,y=300)

    pause_button = Button(window,text="Pause",width=10,bd=1,bg='cyan',font=('Calibri',10))
    pause_button.place(x=200,y= 300)

    window.mainloop()

def browsefiles():
   global listBox
   global song_counter
   global filePathLabel

   try:
      filename = filedialog.askopenfilename()
      HOSTNAME = "127.0.0.1"
      USERNAME = 'lftpd'
      PASSWORD = 'lftpd'

      ftp_server = FTP(HOSTNAME,USERNAME,PASSWORD)
      ftp_server.encoding = 'utf-8'
      ftp_server.cwd('shared_files')
      fname = ntpath.basename(filename)
      with open(filename,'rb') as file:
          ftp_server.storbinary(f"STOR {filename}",file)
      ftp_server.dir()
      ftp_server.quit()

      listBox.insert(song_counter,fname)
      song_counter = song_counter+1

   except FileNotFoundError:
     print('Cancel Button Pressed')

def Download():

   song_to_download =  listBox.get(ANCHOR)
   selectLabel.configure(text="Downloading"+ song_to_download) 
   HOSTNAME = "127.0.0.1"
   USERNAME = 'lftpd'
   PASSWORD = 'lftpd'
   home = str(Path.home())
   download_path = home+ "Downloads"
   ftp_server = FTP(HOSTNAME,USERNAME,PASSWORD)
   ftp_server.encoding = 'utf-8'
   ftp_server.cwd('shared_files')
   local_file_name = os.path.join(download_path,song_to_download)
   file = open(local_file_name,'wb')
   ftp_server.retrbinary("RETR "+ song_to_download,file.write)
   file.close()
   ftp_server.quit()
   selectLabel.configure(text="Download Complete")
   if(song_selected != " "):
       selectLabel.configure(text="NOW PLAYING....."  + song_selected )
   else:
      selectLabel.configure(text=" ")

def setup():
    global SERVER
    global PORT
    global SERVER

    SERVER = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    SERVER.connect((IP_ADDRESS,PORT))

    musicWindow()

setup()