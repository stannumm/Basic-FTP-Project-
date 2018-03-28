from Tkinter import *
import ttk
from ftplib import FTP
import os
from tkFileDialog import askopenfilename
import ntpath


#server dizini
path = "C:/Users/ahmet/Desktop/FTP/"

# bağlantı sağlanması
ftp = FTP("127.0.0.1")
ftp.login(user="user",passwd="12345") #login

root = Tk()  #tkinter objesi

root.title('FTP')

# dosya ismi değiştirme
def rename(tv1):
    changeDir(tv1)
    if(e.get() == ""):     # entry girilmemesi durumu
        newname = "noname"
    else:
        newname = e.get()
    if(len(os.path.splitext(os.path.basename(tv1.selection()[0]))) > 1):  #file extension handling
        extension = os.path.splitext(os.path.basename(tv1.selection()[0]))[1]
    else:
        extension = ""
    ftp.rename(os.path.basename(tv1.selection()[0]),newname+extension)
    ftp.cwd("/")
    tv1.delete(*tv1.get_children())     #treeviewda ismin gösterimi için yenileme
    isdir(path)


#serverdaki current working directory değşimi
def changeDir(tv1):
    if(tv1.selection() == "()"):
        b = str(tv1.parent(tv1.selection()[0])).replace(path,"/")
        b = b.replace("\\","/")
        ftp.cwd(b)

#serverdan dosya alma fonksiyonu
def download(tv1):
    changeDir(tv1)
    localfile = open(os.path.basename(tv1.selection()[0]),"wb")
    ftp.retrbinary("RETR "+os.path.basename(tv1.selection()[0]),localfile.write,1024)
    print("downloaded")
    localfile.close()
    ftp.cwd("/")

# dosya upload fonksiyonu
def placeFile(tv1):
    changeDir(tv1)
    file = askopenfilename()
    ftp.storbinary("STOR "+ntpath.basename(file),open(file,"rb"))
    ftp.cwd("/")
    print("placed")
    tv1.delete(*tv1.get_children()) #treeviewda dosya gösterimi için yenileme
    isdir(path)

tv1 = ttk.Treeview(root) #tkinter treeview objesi
tv1.grid(row = 1)

#listbox'a dosyalari atma
files = ftp.nlst()


# treeviewda server dosyarlaının gösterimini yapan fonksiyon
def isdir(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if(os.path.join(root)==path):
                tv1.insert("",1,os.path.join(root,name),text = name)
            else:
                tv1.insert(root,1,os.path.join(root,name),text = name)
        for name in dirs:
            if(os.path.join(root)==path):
                tv1.insert("",1,os.path.join(root,name),text = name)
            else:
                tv1.insert(root,1,os.path.join(root,name),text = name)

isdir(path)


#tkinter buttonları ve entrysi

b1=Button(root, text = "Upload",command = lambda: placeFile(tv1))
b1.grid(row = 2,column = 0)

b2 = Button(root, text = "Download", command = lambda : download(tv1))
b2.grid(row = 2, column = 1)

b3=Button(root, text = "Rename",command = lambda: rename(tv1))
b3.grid(row = 3 , column = 0)

e = Entry(root, bd =5)
e.grid(column = 1, row = 3)

root.mainloop()

