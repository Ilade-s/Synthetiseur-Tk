from tkinter import * # GUI
from tkinter import ttk # "modern" widgets
from inst_partition import * # Instrument and Partition classes
from functools import partial # to execute function in tkinter with parameters

__VERSION__ = '1.1'
__AUTHOR__ = 'Merlet Raphaël'

# Size of the window (can be resized)
X = 1000
Y = 600
# keyboard keys used to play (can be customized as long as it is 7 keys long)
KEYBOARD_KEYS = ['d', 'f', 'g', 'h', 'j', 'k', 'l']

class Synth(Tk): # Global window/GUI
    def __init__(self, inst='PIANO_MED_', octaves=(5,)) -> None:
        super().__init__()
        self.instrument = Instrument(inst, octaves)
        self.partition = ''
        self.clavier = Clavier(self)
        self.iconphoto(True, PhotoImage(file="Assets/music.png"))
        self.title(
            f"Synthétiseur v{__VERSION__}")   
        self.geometry("{}x{}".format(X, Y))
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
        
        def reset_partition():
            resetButton['state'] = 'active'
            resetButton.update()
            self.partition = ''
            sleep(.1)
            resetButton['state'] = 'normal'

        # bindings for general action (quitting, ...)
        self.bind('<Escape>', lambda e: self.destroy())
        self.bind('<Return>', lambda e: play_music())
        self.bind('<BackSpace>', lambda e: remove_note())
        self.bind('<Delete>', lambda e: reset_partition())
        self.bind('<FocusIn>', lambda e: self.clavier.focus_set())
        # images used for the play and delete buttons
        self.playImage = PhotoImage(file='assets/play.png')
        self.delImage = PhotoImage(file='assets/delete.png')
        self.resetImage = PhotoImage(file='assets/trash.png')
        # play button
        resetButton = ttk.Button(self, text="Reset", command=reset_partition, image=self.resetImage)
        resetButton.place(relx=.15, rely=.75, relwidth=.15, relheight=.15)
        # play button
        playButton = ttk.Button(self, text="Play", command=play_music, image=self.playImage)
        playButton.place(relx=.425, rely=.75, relwidth=.15, relheight=.15)
        # delete button
        removeButton = ttk.Button(self, text="Del", command=remove_note, image=self.delImage)
        removeButton.place(relx=.7, rely=.75, relwidth=.15, relheight=.15)


class Clavier(Frame): # Keys of the instrument
    def __init__(self, master) -> None:
        super().__init__(master, background="#292D3E", relief=RAISED)
        self.create_keys()
        self.place(relx=.05, rely=.05, relwidth=.9, relheight=.6)
    
    def create_keys(self):
        def add_note(note, tempo='n'):
            self.master.partition += note+str(self.master.instrument.octaves[0])+tempo
            self.master.instrument.jouer(note+str(self.master.instrument.octaves[0]), .1)
            self.focus_set()
        
        def key_pressed(event):
            note = notes[KEYBOARD_KEYS.index(event.char)].capitalize()
            self.keys[note]['state'] = 'active'
            self.unbind(event.char)
            self.keys[note].update()
            add_note(note)
            self.keys[note]['state'] = 'normal'
            sleep(.1)

        notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] # notes de musique
        self.keys = {}
        for note, notec in zip(notes, KEYBOARD_KEYS):
            # bindings
            self.bind(notec, key_pressed)
            self.bind(f'<KeyRelease-{notec}>', lambda event: self.bind(event.char, key_pressed))
            # key placing
            key = ttk.Button(self, text=f' {note}\n({notec})', command=partial(add_note, note), style="Keys.TButton")
            key.place(relx=1/len(notes)*notes.index(note), rely=0, relwidth=1/len(notes), relheight=1)
            self.keys[note] = key

        self.focus_set() # to detect keyboard
        
        # creation style
        s = ttk.Style(self)
        s.configure("Keys.TButton", font=("Arial", 35))
        s.configure("Pressedkey.TButton", font=("Arial", 35), bg='#AE3939')


if __name__ == '__main__':
    print("===============================================================")
    print(f"Synth app v{__VERSION__}")
    print(f"Made by {__AUTHOR__}")
    print("Assets : https://feathericons.com/")
    print("===============================================================")

    win = Synth() # the instrument can be chosen here
    #win = Synth('bfx')
    win.mainloop()
    
