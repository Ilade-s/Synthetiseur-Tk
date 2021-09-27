import simpleaudio
from time import sleep

class Instrument:
    def __init__(self, inst, octaves=[i for i in range(8)]) -> None:
        self.type = inst
        self.octaves = octaves
        self.notes = {}
        self.playing = {}
        notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        for o in octaves:
            for n in notes:
                self.notes[n+str(o)] = simpleaudio.WaveObject.from_wave_file('wav/'+inst+n+str(o)+'.wav')

    def jouer(self, note):
        if note in self.playing.keys() and self.playing[note].is_playing():
            self.playing[note].stop()
        self.playing[note] = self.notes[note].play()

class Partition:
    def __init__(self, notes: str, instrument, tempo=.5) -> None:
        self.durees = {
            'a': tempo*8,
            'r': tempo*4,
            'b': tempo*2,
            'n': tempo,
            'c': tempo/2,
            'd': tempo/4,
            't': tempo/8
        }
        self.notes = notes
        self.instrument = instrument
    
    def prepare(self):
        notes_list = [self.notes[i:i+3] for i in range(0, len(self.notes), 3)]
        self.music = [(n[:-1], self.durees[n[-1]]) for n in notes_list]
    
    def play(self):
        for note in self.music:
            self.instrument.jouer(note[0])
            sleep(note[1])

if __name__ == '__main__':
    musique = "C4nC4nC4nD4nE4bD4bC4nE4nD4nD4nC4bC4nC4nC4nD4nE4bD4bC4nE4nD4nD4nC4bD4nD4nD4nD4nA3bA3bD4nC4nB3nA3nG3bC4nC4nC4nD4nE4bD4bC4nE4nD4nD4nC4b"
    #piano1 = Instrument('PIANO_LOUD_', [3, 4])
    piano2 = Instrument('PIANO_MED_', [3, 4])

    partition = Partition(musique, piano2, .5)
    partition.prepare()
    partition.play()

    
