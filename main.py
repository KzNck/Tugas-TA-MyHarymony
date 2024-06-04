from tkinter import filedialog
from tkinter import *
import pygame
import os
import random
import sys

class MusicPlayer:
    def __init__(self, master):
        self.root = master
        self.root.title('MyHarmony')
        self.root.geometry("500x340")

        pygame.mixer.init()

        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        self.songs = []
        self.current_song = ""
        self.paused = False
        self.loop = False  # Variable to store loop status

        self.create_menu()
        self.create_songlist()
        self.create_control_buttons()

        pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Set custom event when music ends

        # Initialize the Pygame display to handle events properly
        pygame.display.set_mode((100, 100))

        # Call handle_events periodically to handle custom events
        self.handle_events()

    def create_menu(self):
        organize_menu = Menu(self.menubar, tearoff=False)
        organize_menu.add_command(label='Select Folder', command=self.load_music)
        self.menubar.add_cascade(label='Organise', menu=organize_menu)

    def create_songlist(self):
        self.songlist = Listbox(self.root, bg="black", fg="white", width=100, height=15)
        self.songlist.pack()
        self.songlist.bind("<Double-Button-1>", self.play_selected_song)

    def create_control_buttons(self):
        self.play_img = PhotoImage(file=r'play.png')
        self.pause_img = PhotoImage(file=r'pause.png')
        self.next_img = PhotoImage(file=r'next.png')
        self.prev_img = PhotoImage(file=r'prev.png')
        self.shuffle_img = PhotoImage(file=r'shuffle.png')

        controlframe = Frame(self.root)
        controlframe.pack()

        self.play = Button(controlframe, image=self.play_img, borderwidth=0, command=self.play_music)
        self.pause = Button(controlframe, image=self.pause_img, borderwidth=0, command=self.pause_music)
        self.next = Button(controlframe, image=self.next_img, borderwidth=0, command=self.next_music)
        self.prev = Button(controlframe, image=self.prev_img, borderwidth=0, command=self.prev_music)
        self.shuffle = Button(controlframe, image=self.shuffle_img, borderwidth=0, command=self.shuffle_music)

        self.play.grid(row=0, column=1, padx=7, pady=10)
        self.pause.grid(row=0, column=2, padx=7, pady=10)
        self.next.grid(row=0, column=3, padx=7, pady=10)
        self.prev.grid(row=0, column=0, padx=7, pady=10)
        self.shuffle.grid(row=0, column=4, padx=7, pady=10)

        self.loop_on = Button(controlframe, text="Loop On", command=self.loop_on)
        self.loop_off = Button(controlframe, text="Loop Off", command=self.loop_off)
        self.loop_on.grid(row=1, column=1, padx=7, pady=10)
        self.loop_off.grid(row=1, column=2, padx=7, pady=10)

        self.loop_status = Label(controlframe, text="Loop: Off")
        self.loop_status.grid(row=1, column=3, padx=7, pady=10)

    def load_music(self):
        self.root.directory = filedialog.askdirectory()

        # Clear existing songs
        self.clear_songlist()

        for song in os.listdir(self.root.directory):
            name, ext = os.path.splitext(song)
            if ext == '.mp3':
                self.songs.append(song)
        
        for song in self.songs:
            self.songlist.insert("end", song)

        self.songlist.selection_set(0)
        self.current_song = self.songs[self.songlist.curselection()[0]]

    def clear_songlist(self):
        self.songlist.delete(0, END)
        self.songs.clear()

    def play_selected_song(self, event):
        selected_index = self.songlist.curselection()[0]
        self.current_song = self.songs[selected_index]
        self.play_music()

    def play_music(self):
        if not self.paused:
            pygame.mixer.music.load(os.path.join(self.root.directory, self.current_song))
            if self.loop:
                pygame.mixer.music.play(loops=-1)  # Infinite loop
            else:
                pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()
            self.paused = False

    def pause_music(self):
        pygame.mixer.music.pause()
        self.paused = True

    def next_music(self):
        selected_indices = self.songlist.curselection()
        if selected_indices:  # Check if there's at least one item selected
            self.songlist.selection_clear(0, END)
            next_index = (selected_indices[0] + 1) % len(self.songs)  # Calculate the index of the next song
            self.songlist.selection_set(next_index)
            self.current_song = self.songs[next_index]
            self.play_music()

    def prev_music(self):
        try:
            selected_indices = self.songlist.curselection()
            if selected_indices:  # Check if there's at least one item selected
                self.songlist.selection_clear(0, END)
                prev_index = (selected_indices[0] - 1) % len(self.songs)  # Calculate the index of the previous song
                self.songlist.selection_set(prev_index)
                self.current_song = self.songs[prev_index]
                self.play_music()
        except IndexError:
            pass

    def shuffle_music(self):
        random.shuffle(self.songs)
        self.songlist.delete(0, END)
        for song in self.songs:
            self.songlist.insert("end", song)
        self.current_song = self.songs[0]
        self.songlist.selection_clear(0, END)
        self.songlist.selection_set(0)
        if not self.paused:
            pygame.mixer.music.load(os.path.join(self.root.directory, self.current_song))
            if self.loop:
                pygame.mixer.music.play(loops=-1)  # Infinite loop
            else:
                pygame.mixer.music.play()

    def loop_on(self):
        self.loop = True
        self.loop_status.config(text="Loop: On")
        if pygame.mixer.music.get_busy():  # If music is currently playing
            pygame.mixer.music.play(loops=-1)  # Set to infinite loop

    def loop_off(self):
        self.loop = False
        self.loop_status.config(text="Loop: Off")
        if pygame.mixer.music.get_busy():  # If music is currently playing
            pos = pygame.mixer.music.get_pos()  # Get current position
            pygame.mixer.music.load(os.path.join(self.root.directory, self.current_song))
            pygame.mixer.music.play(start=pos/1000.0)  # Restart song from current position

    def play_next_song(self):
        selected_index = self.songlist.curselection()[0]
        next_index = (selected_index + 1) % len(self.songs)
        self.songlist.selection_clear(0, END)
        self.songlist.selection_set(next_index)
        self.current_song = self.songs[next_index]
        self.play_music()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:  # Custom event when music ends
                self.play_next_song()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Call this method again after a short delay to keep checking for events
        self.root.after(100, self.handle_events)

root = Tk()
music_player = MusicPlayer(root)
root.mainloop()
