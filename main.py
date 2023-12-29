from tkinter import *
from tkinter import filedialog
import ctypes as ct
import pygame
import os

window = Tk()

def dark_title_bar(window):  # obtained via stack overflow at https://stackoverflow.com/questions/23836000/can-i-change-the-title-bar-in-tkinter
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))


background_color = "#232323"



try:                        #If user isn't on windows 11, function might not work, so they won't have the dark bar
    dark_title_bar(window)
except Exception:
    pass



icon = PhotoImage(file='mp_icon_inpngformat.png.')
play_button_icon = PhotoImage(file="play_button.png")
pause_button_icon = PhotoImage(file="pause_button.png")
rewind_button_icon = PhotoImage(file="rewind_button.png")
skip_button_icon = PhotoImage(file="skip_button.png")
beat_pic_icon = PhotoImage(file="beat.png")


window.title("Music Player")
window.geometry("1000x1000")
window.iconphoto(True, icon)
window.config(background="#232323")


pygame.mixer.init()
songs = []
current_song = ""
paused = False

def load_folder():
    global current_song
    window.directory = filedialog.askdirectory()

    for song in os.listdir(window.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)
    for song in songs:
        songlist.insert("end", song)

    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]


songlist = Listbox(window, bg=background_color, fg="white", width=200, height=13)
songlist.pack()

menubar = Menu(window)
window.config(menu=menubar)

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder for music',command=load_folder)
menubar.add_cascade(label="Organize", menu=organise_menu)


def press_play():
    global current_song, paused

    if not paused:
        pygame.mixer.music.load(os.path.join(window.directory,current_song))
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

def press_pause():
    global paused
    pygame.mixer.music.pause()
    paused = True


def press_skip():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) + 1)
        current_song = songs[songlist.curselection()[0]]
        press_play()
    except:
        pass

def press_rewind():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]]
        press_play()
    except:
        pass

label = Label(window, text=f"", font=("Arial", 20), foreground='white', background=background_color)
label.pack()

canvas = Canvas(window, width=330, height=550,background=background_color,borderwidth=0)
canvas.pack(side=BOTTOM)
canvas.create_image(0, 0, anchor=NW, image=beat_pic_icon)

def set_volume(val):
    volme = int(val) / 100
    pygame.mixer.music.set_volume(volme)

volume_slider = Scale(window,from_=100,to=0, command=set_volume)
volume_slider.pack(side=RIGHT,padx = 10)

rewind_button = Button(window, image= rewind_button_icon, command= press_rewind, state= ACTIVE, activebackground= background_color, background= background_color, borderwidth=0)
rewind_button.pack(side=LEFT,padx = 20)

play_button = Button(window, image=play_button_icon,command= press_play, state=ACTIVE,activebackground= background_color, background=background_color,borderwidth=0)
play_button.pack(side=LEFT,padx = 20,)


pause_button = Button(window, image= pause_button_icon,command= press_pause, state=ACTIVE, activebackground= background_color, background=background_color, borderwidth=0)
pause_button.pack(side=LEFT,padx = 20)

skip_button = Button(window, image= skip_button_icon,command=press_skip, state=ACTIVE, activebackground= background_color, background= background_color, borderwidth=0)
skip_button.pack(side=LEFT,padx = 20)



window.mainloop()