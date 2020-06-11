
"""
@author: Manish Wadile
"""

import os
import os.path
import pygame
import time
import threading
import pandas as pd
import xlsxwriter
import tkinter.messagebox
from tkinter.filedialog import askdirectory,askopenfilename
from tkinter import Tk,Menu,Frame,BOTTOM,LEFT,TOP,RIGHT,PhotoImage,Label,Button,Listbox,HORIZONTAL,NO,Y,BOTH,X,StringVar
from tkinter import ttk
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen.mp3 import MP3
from PIL import Image,ImageTk
from io import BytesIO
from pynput.keyboard import Key,Controller


#--------------Splash----------------------------
"""def cpause():
    icon['image']=pauseico

def call_mainroot():
    splash.destroy()

splash=Tk()
splash.minsize(300,150)
windowWidth = splash.winfo_reqwidth()
windowHeight = splash.winfo_reqheight()
positionRight = int(splash.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(splash.winfo_screenheight()/2 - windowHeight/2)
splash.geometry("+{}+{}".format(positionRight, positionDown))
playico=PhotoImage(file=r"icons\play.png")
pauseico=PhotoImage(file=r"icons\pause.png")
icon=Label(splash,image=playico,font='Times 25 bold',bg='#2f3640',fg='white')
icon.pack()
splash.overrideredirect(True)
splash.configure(background='#2f3640')
splash.after(1000,cpause)               
splash.after(3000,call_mainroot)
splash.mainloop()"""

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=




keyboard=Controller()
root=Tk()
root.minsize(300,200)
root.resizable(0,0)
root.iconbitmap(r'icons\player.ico')
root.title("BreakDown Music Player")

#-----------------Menubar------------------
def aboutus():
    tkinter.messagebox.showinfo('About us','Developer - Manish Wadile\nIcon software - Iconion')

def exitthis():
    pygame.mixer.music.stop()
    root.destroy()

menubar=Menu(root,bg='#2f3640')
root.config(bg='#2f3640',menu=menubar)
file=Menu(menubar,tearoff=0)
menubar.add_cascade(label="File",menu=file)
file.add_command(label="Exit",command=exitthis)

about=Menu(menubar,tearoff=0)
menubar.add_cascade(label="About",menu=about)
about.add_command(label="About us",command=aboutus)





#----------------------------------------------

listofsongs=[]
realnames=[]
posters=[]
artist=[]
track=[]
release=[]
index=0
volume=0
ssetstat=3
playing=False
stop_thread=False
root.configure(background='#2f3640')
v=StringVar()

#---------------------Frames-------------------------------
upper_f=Frame(root,bg='#2f3640')
upper_f.pack(side=TOP)
player = Frame(upper_f,bg='#2f3640')
player.pack( side = LEFT)
sugge=Frame(root,bg='#2f3640')
sugge.pack(side=BOTTOM)
s_photo=Frame(player,bg='#2f3640')
s_photo.pack(side=TOP)
s_stat=Frame(player,bg='#2f3640')
s_stat.pack(side=TOP)
s_controls=Frame(player,bg='#2f3640')
s_controls.pack(side=TOP)

s_list=Frame(upper_f,bg='#2f3640')
s_list.pack(side=RIGHT)
listcon=Frame(sugge,bg='#2f3640')
listcon.pack(side=LEFT)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


songlabel=Label(s_photo,textvariable=v,width=50,font='Ms-Serif 15 bold',bg='#2f3640',fg='white')

                
#-------------Icons--------------------------------------------                
songico=PhotoImage(file=r"icons\song.png")
canvas = Label(s_photo,image=songico)
nextico=PhotoImage(file=r"icons\next.png")
preico=PhotoImage(file=r"icons\previous.png")
for5ico=PhotoImage(file=r"icons\for5.png")
playico=PhotoImage(file=r"icons\play.png")
pauseico=PhotoImage(file=r"icons\pause.png")
volumico=PhotoImage(file=r"icons\speaker.png")
volume_hover=PhotoImage(file=r"icons\speaker_hover.png")
defaultcover=PhotoImage(file=r"icons\song.png")
for5_hover=PhotoImage(file=r"icons\for5_hover.png")
nxt_hover=PhotoImage(file=r"icons\nxt_hover.png")
pre_hover=PhotoImage(file=r"icons\pre_hover.png")
play_hover=PhotoImage(file=r"icons\play_hover.png")
pause_hover=PhotoImage(file=r"icons\pause_hover.png")
loop=PhotoImage(file=r"icons\loop.png")
loop_hover=PhotoImage(file=r"icons\loop_hover.png")
likeico=PhotoImage(file=r"icons\like.png")
like_hover=PhotoImage(file=r"icons\like_hover.png")
likedico=PhotoImage(file=r"icons\liked.png")
liked_hover=PhotoImage(file=r"icons\liked_hover.png")
muteico=PhotoImage(file=r"icons\mute.png")
mute_hover=PhotoImage(file=r"icons\mute_hover.png")
lowvol=PhotoImage(file=r"icons\lowvol.png")
lowvol_hover=PhotoImage(file=r"icons\lowvol_hover.png")
novol=PhotoImage(file=r"icons\no_vol.png")
novol_hover=PhotoImage(file=r"icons\no_vol_hover.png")
playlist=PhotoImage(file=r"icons\playlist.png")
playlist_hover=PhotoImage(file=r"icons\playlist_hover.png")
addico=PhotoImage(file=r"icons\add.png")
add_hover=PhotoImage(file=r"icons\add_hover.png")
folder=PhotoImage(file=r"icons\folder.png")
folder_hover=PhotoImage(file=r"icons\folder_hover.png")
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

class Scale(ttk.Scale):
    def __init__(self, master=None, **kwargs):
        ttk.Scale.__init__(self, master, **kwargs)
        self.bind('<Button-1>', self.set_value)

    def set_value(self, event):
        self.event_generate('<Button-3>', x=event.x, y=event.y)
        return 'break'





# ---------Song recommandation system---------------------------------
         
def filldata():
    not_match=[]
    homedir = os.path.expanduser("~")
    if(os.path.isfile(homedir+'/m_data.xlsx')):
        datafile=homedir+"/m_data.xlsx"
        dataxl=pd.read_excel(datafile)
        i=1
        not_match.clear()
        try:
            while(len(str(dataxl.iloc[i,0]))!=0):
                if str(dataxl.iloc[i,0])==listofsongs[i]:
                    pass
                else:
                    not_match.append(listofsongs[i])
                i+=1
        except IndexError:
            if len(not_match)!=0:
                temp=i
                for i in range(0,len(not_match)):
                    data=[{'song_name':not_match[i],'times_played':0,'times_cliked':0,'path':os.path.realpath(not_match[i]),'like_stat':0}]
                    #dataxl.append(data,ignore_index=True,sort=False)
                    dataxl.loc[temp+i]=list(data[0].values())
                dataxl.to_excel(datafile,sheet_name='Sheet1',index=False)
        song_name=[]
        song_path=[]
        values=[]
        like_stat=[]
        f_list=[]
        try:
            tptotal=int(dataxl[['times_played']].sum())
            tctotal=int(dataxl[['times_cliked']].sum())
            for i in range(0,int(dataxl[['song_name']].count())-1):
                song_name.append(dataxl.iloc[i,0])
                values.append((dataxl.iloc[i,1]/tptotal)+(dataxl.iloc[i,2]/tctotal))
                song_path.append(dataxl.iloc[i,3])
                like_stat.append(dataxl.iloc[i,4])
            tempval=values
            """print(values)
            # to convert lists to dictionary 
            s_prob = {song_name[i]: float(values[i]) for i in range(len(song_name))}
            print(s_prob)
            #dd = {k: v for k, v in sorted(s_prob.items(), key=lambda item: item[1])}
            #print(dd)"""
            tempval.sort(reverse=True)
            marked=[]
            try:
                for i in range(0,int(dataxl[['song_name']].count())-1):
                    if(tempval[i]!=0):
                        idx=values.index(tempval[i])
                        if idx in marked:
                            idx+=1
                            print(" pass1 ")
                            for j in range(idx,len(values)):
                                if values[j]==tempval[i]:
                                    f_list.append(song_name[j])
                                    marked.append(j)
                                    print(" pass2 ")
                                    print(" "+str(idx)+" ")
                        else:
                            f_list.append(song_name[idx])
                            marked.append(idx)
                            print(" "+str(idx)+" ")
                print(f_list)    
                f_list.reverse()
                for items in f_list:
                    suggbox.insert(0,items)
            except ZeroDivisionError:
                pass
        except ZeroDivisionError:
            print("There is no data to show")
            
                
            
    else:
        workbook=xlsxwriter.Workbook(homedir+'/m_data.xlsx')
        worksheet=workbook.add_worksheet()
        worksheet.write('A1', 'song_name')
        worksheet.write('B1', 'times_played')
        worksheet.write('C1', 'times_cliked')
        worksheet.write('D1', 'path')
        worksheet.write('E1', 'like_stat')
        for i in range(0,len(listofsongs)):
            a="A"+str(i+2)
            b="B"+str(i+2)
            c="C"+str(i+2)
            d="D"+str(i+2)
            e="E"+str(i+2)
            worksheet.write(a,listofsongs[i])
            worksheet.write(b,0)
            worksheet.write(c,0)
            worksheet.write(d,os.path.realpath(listofsongs[i]))
            worksheet.write(e,0)
        workbook.close()
        
            


#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#------Player Functions-------------------------------------------

def playpause(e):
    global playing
    if(playpausebtn['text']=='Pause'):
        playpausebtn['text']='Play'
        playpausebtn['image']=playico
        pygame.mixer.music.pause()
        playing=True
        
    else:
        playpausebtn['text']= 'Pause'
        playpausebtn['image']=pauseico
        pygame.mixer.music.unpause()
        playing=False   
         


def set_vol(val):
    global volume
    if(float(val)<20):
        speaker['text']='20'
        speaker['image']=novol
    elif(float(val)<70):
        speaker['text']='70'
        speaker['image']=lowvol
    else:
        speaker['text']='100'
        speaker['image']=volumico
    volume=float(val)/100
    pygame.mixer.music.set_volume(volume)



def set_song_pos(val):
    global songpos,total_length,current_time,ssetstat
    if(ssetstat==1):
        ssetstat=0
    elif(ssetstat==0):
        clickedtime=float(val)
        print(clickedtime)
        pygame.mixer.music.rewind()
        pos=int(clickedtime/(1000/total_length))
        print(pos)
        songpos=pos
        current_time=pos
        pygame.mixer.music.play(start=pos)
        
    
    
    


def playnext(event):
    global index,t,current_time,songpos,total_length
    index += 1
    pygame.mixer.music.stop()
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    current_time=0
    songpos=0
    audio=MP3(os.path.realpath(listofsongs[index]))
    t=audio.info.length
    updatelabel()
    if(playpausebtn['text']=='Play'):
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        t1 = threading.Thread(target=start_count, args=(total_length,))
        t1.start()
    homedir = os.path.expanduser("~")
    datafile=homedir+"/m_data.xlsx"
    dataxl=pd.read_excel(datafile)
    i=0
    j=-1
    while j<1:
        if songlabel['text'] == str(dataxl.iloc[i,0]):
            if dataxl.iloc[i,4]==1 :
                likebtn['image']=likedico
                likebtn['text']="liked"
            else:
                likebtn['text']='like'
                likebtn['image']=likeico
            j=3
                
        i+=1

        

def playpre(event):
    global index,current_time,t,songpos,total_length
    index -= 1
    pygame.mixer.music.stop()
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    current_time=0
    songpos=0
    audio=MP3(os.path.realpath(listofsongs[index]))
    t=audio.info.length
    updatelabel()
    if(playpausebtn['text']=='Play'):
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        t1 = threading.Thread(target=start_count, args=(total_length,))
        t1.start()
    homedir = os.path.expanduser("~")
    datafile=homedir+"/m_data.xlsx"
    dataxl=pd.read_excel(datafile)
    i=0
    j=-1
    while j<1:
        if songlabel['text'] == str(dataxl.iloc[i,0]):
            if dataxl.iloc[i,4]==1 :
                likebtn['image']=likedico
                likebtn['text']="liked"
            else:
                likebtn['text']='like'
                likebtn['image']=likeico
            j=3
                
        i+=1
        

    
def add_song(e):
    file=askopenfilename()
    listofsongs.append(file)
    listbox.delete(0,'end')
    listofsongs.reverse()
    for items in listofsongs:
        listbox.insert(0,items)
    listofsongs.reverse()


def dirchooser():
    global total_length,stop_thread
    listofsongs.clear()
    posters.clear()
    artist.clear()
    track.clear()
    listbox.delete(0,'end')
    directory=askdirectory()
    os.chdir(directory)
    try:
        if t1.is_alive():
            stop_thread=True
    except UnboundLocalError:
        pass
    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir=os.path.realpath(files)       
            try:
                #audio=ID3(realdir)
                tags = ID3(realdir)
                try:
                    pict = tags.get("APIC:").data
                    im = Image.open(BytesIO(pict))
                    im = im.resize((256, 256), Image.ANTIALIAS)
                    tkim = ImageTk.PhotoImage(im)
                    posters.append(tkim)
                except AttributeError:
                    posters.append(songico)
            except ID3NoHeaderError:
                pass
                #audio = ID3()
            try:
                artist.append(tags.get("TPE1"))
            except ID3NoHeaderError:
                artist.append("0")
            try:
                track.append(tags.get("TIT2"))
            except ID3NoHeaderError:
                track.append("0")
            try:
                release.append(tags.get("TDRC"))
            except ID3NoHeaderError:
                release.append("0")
            listofsongs.append(files)
    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    updatelabel()
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    listofsongs.reverse()
    for items in listofsongs:
        listbox.insert(0,items)
    listofsongs.reverse()
    filldata()
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=    
    
#-------------Thread----------------------------------------
def start_count(t):
    global playing,stop_thread,songpos
    global current_time,total_length,ssetstat
    current_time=0
    songpos=0
    while current_time <= t and pygame.mixer.music.get_busy():
        if stop_thread:
            stop_thread=False
            current_time=0
            break
        elif playing:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            c_time['text'] = timeformat
            time.sleep(1)
            current_time += 1
            songpos += 1
            ssetstat=1
            stat.set((1000/total_length)*songpos)
            ssetstat=0
        print("running")

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=   


#-------------------Hover Functions---------------------------------
def select(e):
    homedir = os.path.expanduser("~")
    datafile=homedir+"/m_data.xlsx"
    dataxl=pd.read_excel(datafile)
    i=1
    try:
        while(len(str(dataxl.iloc[i,0]))!=0):
            if str(dataxl.iloc[i,0])==listbox.get(listbox.curselection()):
                dataxl.iloc[i,2]+=1
                dataxl.to_excel(datafile,sheet_name='Sheet1',index=False)
                break
            i+=1
    except IndexError:
        pass


def nxtenter(e):
    nxtbtn['image']=nxt_hover

def nxtleave(e):
    nxtbtn['image']=nextico

def preenter(e):
    prebtn['image']=pre_hover

def preleave(e):
    prebtn['image']=preico

def for5(e):
    global current_time,songpos
    songpos += 5
    current_time += 5
    pygame.mixer.music.play(start=songpos)    

def for5enter(e):
    forbtn['image']=for5_hover

def for5leave(e):
    forbtn['image']=for5ico

def ppenter(e):
    if(playpausebtn['text']=='Pause'):
        playpausebtn['image']=pause_hover
    else:
        playpausebtn['image']=play_hover
def ppleave(e):
    if(playpausebtn['text']=='Pause'):
        playpausebtn['image']=pauseico
    else:
        playpausebtn['image']=playico

def likeenter(e):
    if(likebtn['text']=='like'):
        likebtn['image']=like_hover
    else:
        likebtn['image']=liked_hover
def likeleave(e):
    if(likebtn['text']=='like'):
        likebtn['image']=likeico
    else:
        likebtn['image']=likedico
def like(e):
    if(likebtn['text']=='liked'):
        likebtn['text']='like'
        likebtn['image']=likeico
        homedir = os.path.expanduser("~")
        datafile=homedir+"/m_data.xlsx"
        dataxl=pd.read_excel(datafile)
        i=0
        j=-1
        while j<1:
            if songlabel['text'] == str(dataxl.iloc[i,0]):
                dataxl.iloc[i,4]=0
                j=3
                
            i+=1
        dataxl.to_excel(datafile,sheet_name='Sheet1',index=False)
    else:
        likebtn['image']=likedico
        likebtn['text']="liked"
        homedir = os.path.expanduser("~")
        datafile=homedir+"/m_data.xlsx"
        dataxl=pd.read_excel(datafile)
        i=0
        j=-1
        while j<1:
            if songlabel['text'] == str(dataxl.iloc[i,0]):
                dataxl.iloc[i,4]=1
                j=3
                
            i+=1
        dataxl.to_excel(datafile,sheet_name='Sheet1',index=False)



            
def clkplayl(e):
    def exitfun():
        listw.destroy()
        root.deiconify() 
    homedir = os.path.expanduser("~")
    if(os.path.isdir(homedir+'/myplaylist/')):
        print("path exist")
    else:
        os.mkdir(homedir+'/myplaylist')
        print("path not exist ! file created !")
        
    listw=Tk()
    listw.minsize(200,400)
    root.withdraw()
    listw.configure(background='#2f3640')
    windowWidth = listw.winfo_reqwidth()
    windowHeight = listw.winfo_reqheight()
    positionRight = int(listw.winfo_screenwidth()/2 - windowWidth/2)-200
    positionDown = int(listw.winfo_screenheight()/2 - windowHeight/2)-200
    listw.geometry("+{}+{}".format(positionRight, positionDown))
    toplbl=Label(listw,text="Playlist's",bg='#2f3640',fg='white')
    toplbl.pack(side=TOP)
    tree=ttk.Treeview(listw)
    tree["columns"]=("name","no_songs")
    tree.column("#0",width=60,minwidth=30,stretch=NO)
    tree.column("name",width=60,minwidth=60,stretch=NO)
    tree.column("no_songs",width=60,minwidth=30,stretch=NO)
    tree.heading('#0',text='Icon',anchor='center')
    tree.heading('name',text='name',anchor='center')
    tree.heading('no_songs',text='No of songs',anchor='center')
    tree.insert("","1",text="1",open=True,image=playlist,values=("My playlist","30"))
    tree.pack(side=TOP,fill=X)
                
    exitbtn=ttk.Button(listw,text='Exit',command=exitfun)
    exitbtn.pack(side=TOP)
    listw.overrideredirect(True)
    listw.mainloop()
        
        

def spk(e):
    global volume
    if(speaker['text']=='mute'):
        if(volume*100<20):
            speaker['text']='20'
            speaker['image']=novol
            pygame.mixer.music.set_volume(volume)
        elif(volume*100<70):
            speaker['text']='70'
            speaker['image']=lowvol
            pygame.mixer.music.set_volume(volume)
        else:
            speaker['text']='100'
            speaker['image']=volumico
            pygame.mixer.music.set_volume(volume)
    else:
        speaker['text']='mute'
        speaker['image']=muteico
        pygame.mixer.music.set_volume(0.0)

def spkleave(e):
    if(speaker['text']=='20'):
        speaker['image']=novol
    elif(speaker['text']=='70'):
        speaker['image']=lowvol
    elif(speaker['text']=='mute'):
        speaker['image']=muteico
    else:
        speaker['text']='100'
        speaker['image']=volumico

def spkenter(e):
    if(speaker['text']=='20'):
        speaker['image']=novol_hover
    elif(speaker['text']=='70'):
        speaker['image']=lowvol_hover
    elif(speaker['text']=='mute'):
        speaker['image']=mute_hover
    else:
        speaker['text']='100'
        speaker['image']=volume_hover
        
def addenter(e):
    addbtn['image']=add_hover

def addleave(e):
    addbtn['image']=addico

def foldenter(e):
    foldbtn['image']=folder_hover

def foldleave(e):
    foldbtn['image']=folder

def playlenter(e):
    playlistbtn['image']=playlist_hover

def playlleave(e):
    playlistbtn['image']=playlist

def clkfold(e):
    dirchooser()

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-

def updatelabel():
    global index
    global songname
    global t1,total_length
    v.set(listofsongs[index])
    audio=MP3(os.path.realpath(listofsongs[index]))
    total_length=audio.info.length
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    c_totaltime['text']=timeformat
    c_time['text']="00:00"
    stat.set(0)
    canvas['image']=posters[index]
    pygame.mixer.music.play()
    
    



#----------------GUI---------------------
scrollbar = ttk.Scrollbar(sugge)
scrollbar.pack(side=RIGHT, fill=Y)
suggelbl=Label(s_list,font='Helvetica 13 bold',text='Hand-picked for you!',bg='#2f3640',fg='white')
suggelbl.pack()
listbox=Listbox(sugge,width=120,bd=0,bg='#2f3640',fg='white',cursor='hand2',selectbackground='black')
listbox.pack(side=RIGHT,fill=BOTH)
suggbox=Listbox(s_list,width=30,height=20,bg='#2f3640',fg='white')
suggbox.pack(side=RIGHT,fill=BOTH)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
#list buttons
addbtn=Button(listcon,text='Previous',image=addico,bg='#2f3640',highlightthickness = 0,bd=0,cursor='hand2')
addbtn.pack(side=TOP)
foldbtn=Button(listcon,text='Previous',image=folder,bg='#2f3640',highlightthickness = 0,bd=0,cursor='hand2')
foldbtn.pack(side=TOP)
playlistbtn=Button(listcon,text='Previous',image=playlist,bg='#2f3640',highlightthickness = 0,bd=0,cursor='hand2')
#playlistbtn.pack(side=TOP)


likebtn=Button(s_controls,text='like',image=likeico,bg='#2f3640',highlightthickness = 0,bd=0,cursor='hand2')
likebtn.pack(side=LEFT)
prebtn=Button(s_controls,text='Previous',image=preico,bg='#2f3640',highlightthickness = 0,bd=0,cursor='hand2')
prebtn.pack(side=LEFT)
playpausebtn=Button(s_controls,text='Pause',image=pauseico,bg='#2f3640',highlightthickness = 0,bd=0,cursor='hand2')
playpausebtn.pack(side=LEFT)
nxtbtn=Button(s_controls,image=nextico,bg='#2f3640',highlightthickness = 0,bd=0,cursor='hand2')
nxtbtn.pack(side=LEFT)
forbtn = Button(s_controls,image=for5ico,bg='#2f3640',highlightthickness = 0,bd=0,cursor='hand2')
forbtn.pack(side=LEFT)
speaker = Button(s_controls,text='100',image=volumico,bg='#2f3640',highlightthickness = 0,bd=0,cursor='hand2')     
speaker.pack(side=LEFT)


#-------------Onclick,Onhover,Doubleclick Events------------------------
listbox.bind("<Double-Button-1>",select)
speaker.bind("<Button-1>",spk)
speaker.bind("<Enter>",spkenter)
speaker.bind("<Leave>", spkleave)
likebtn.bind("<Button-1>",like)
likebtn.bind("<Enter>",likeenter)
likebtn.bind("<Leave>", likeleave)
nxtbtn.bind("<Button-1>",playnext)
nxtbtn.bind("<Enter>",nxtenter)
nxtbtn.bind("<Leave>", nxtleave)
prebtn.bind("<Button-1>",playpre)
prebtn.bind("<Enter>",preenter)
prebtn.bind("<Leave>", preleave)
forbtn.bind("<Button-1>",for5)
forbtn.bind("<Enter>",for5enter)
forbtn.bind("<Leave>", for5leave)

addbtn.bind("<Button-1>",add_song)
addbtn.bind("<Enter>",addenter)
addbtn.bind("<Leave>",addleave)
foldbtn.bind("<Button-1>",clkfold)
foldbtn.bind("<Enter>",foldenter)
foldbtn.bind("<Leave>",foldleave)
playlistbtn.bind("<Button-1>",clkplayl)
playlistbtn.bind("<Enter>",playlenter)
playlistbtn.bind("<Leave>",playlleave)

playpausebtn.bind("<Button-1>",playpause)
playpausebtn.bind("<Enter>",ppenter)
playpausebtn.bind("<Leave>", ppleave)
root.bind("<space>",playpause,)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

canvas.pack()
songlabel.pack()
 
ttk.Style().configure("TScale", padding=6, relief="flat",background="#2f3640")
scale=ttk.Scale(s_controls,from_=0,to=100,orient=HORIZONTAL,command=set_vol,cursor='hand2')
scale.pack(side=LEFT)
c_time=Label(s_stat,text='00:00',bg='#2f3640',fg='white')
c_time.pack(side=LEFT)
stat=Scale(s_stat,from_=0,to=1000,length=300,orient=HORIZONTAL,command=set_song_pos,cursor='hand2')
stat.pack(side=LEFT)

c_totaltime=Label(s_stat,text='00:00',bg='#2f3640',fg='white')
c_totaltime.pack(side=LEFT)
dirchooser()
inivolume=pygame.mixer.music.get_volume()
scale.set(inivolume*100)
#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-
root.protocol("WM_DELETE_WINDOW",exitthis)
root.mainloop()
