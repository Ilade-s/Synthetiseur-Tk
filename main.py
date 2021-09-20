from tkinter import * # GUI
from tkinter import ttk # "modern" widgets
from inst_partition import * # Instrument and Partition classes
from functools import partial # to execute function in tkinter with parameters

__VERSION__ = '0.1'
__AUTHOR__ = 'Merlet Raphaël'

x = 1000
y = 600

class Synth(Tk): # Global window/GUI
    def __init__(self, inst='PIANO_MED_', octaves=(5,)) -> None:
        super().__init__()
        self.instrument = Instrument(inst, octaves)
        self.partition = ''
        self.clavier = Clavier(self)
        self.iconphoto(True, PhotoImage(file="Assets/music.png"))
        self.title(
            f"Synthétiseur v{__VERSION__}")   
        self.geometry("{}x{}".format(x, y))
        self.create_widgets()
    
    def create_widgets(self):
        def play_music():
            playButton['state'] = 'active'
            playButton.update()
            partition = Partition(self.partition, self.instrument)
            partition.prepare()
            partition.play()
            sleep(.1)
            playButton['state'] = 'normal'
        
        def remove_note():
            removeButton['state'] = 'active'
            removeButton.update()
            self.partition = self.partition[:-3]
            sleep(.1)
            removeButton['state'] = 'normal'

        # bindings for general action (quitting, ...)
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Return>', lambda e: play_music())
        self.bind('<Delete>', lambda e: remove_note())
        self.bind('<FocusIn>', lambda e: self.clavier.focus_set())
        # images used for the play and delete buttons
        self.playImage = PhotoImage(file='assets/play.png')
        self.delImage = PhotoImage(file='assets/delete.png')
        # play button
        playButton = ttk.Button(self, text="Play", command=play_music, image=self.playImage)
        playButton.place(relx=.15, rely=.75, relwidth=.15, relheight=.15)
        # delete button
        removeButton = ttk.Button(self, text="Del", command=remove_note, image=self.delImage)
        removeButton.place(relx=.7, rely=.75, relwidth=.15, relheight=.15)


class Clavier(Frame): # Keys of the instrument
    def __init__(self, master) -> None:
        super().__init__(master, background="#292D3E", relief=RAISED)
        self.create_keys()
        self.place(relx=.05, rely=.05, relwidth=.9, relheight=.6)
    
    def create_keys(self):
        def add_note(note, octave=5, tempo='n'):
            self.master.partition += note+str(octave)+tempo
            self.master.instrument.jouer(note+str(octave), .2)
            self.focus_set()
        
        def key_pressed(event):
            note = notes[notes_clavier.index(event.char)].capitalize()
            self.keys[note]['state'] = 'active'
            self.unbind(event.char)
            self.keys[note].update()
            add_note(note)
            self.keys[note]['state'] = 'normal'
            self.bind(event.char, key_pressed)

        notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] # notes de musique
        notes_clavier = ['d', 'f', 'g', 'h', 'j', 'k', 'l'] # keyboard keys used to play
        self.keys = {}
        for note, notec in zip(notes, notes_clavier): # binding and creation of the keys
            self.bind(notec, key_pressed)
            key = ttk.Button(self, text=note, command=partial(add_note, note), style="Keys.TButton")
            key.place(relx=1/len(notes)*notes.index(note), rely=0, relwidth=1/len(notes), relheight=1)
            self.keys[note] = key

        self.focus_set() # to detect keyboard
        
        # creation style
        s = ttk.Style(self)
        s.configure("Keys.TButton", font=("Arial", 40))
        s.configure("Pressedkey.TButton", font=("Arial", 40), bg='#AE3939')


if __name__ == '__main__':
    print("===============================================================")
    print(f"Synth app v{__VERSION__}")
    print(f"Made by {__AUTHOR__}")
    print("Assets : https://feathericons.com/")
    print("===============================================================")

    win = Synth()
    #win = Synth('bfx')
    win.mainloop()
    
