import random
from File import File
from MidiInfo import Note, Rest, Control
from midiutil import MIDIFile


class Translator:
    def __init__(self):
        self.instrument = 0
        self.pitch = 0
        self.octave = 0
        self.volume = 40
        self.bpm = 60
        self.notes = {
            "c": 60,
            "d": 62,
            "e": 64,
            "f": 65,
            "g": 67,
            "a": 69,
            "b": 71,
        }
        self.noteType = None
        self.translatedNotes = []
        self.initialSilence = True

    def reset(self):
        self.instrument = 0
        self.pitch = 0
        self.octave = 0
        self.volume = 40
        self.bpm = 60
        self.notesType = None
        self.translatedNotes = []

    def convertTextToMIDI(self, buffer: str) -> Note | Rest | Control | None:
        if len(buffer) == 0:
            raise ValueError("Buffer is empty")

        if self.instrument == 124:
            self.instrument = 0

        ch = buffer[-1].lower()
        if ch in self.notes:
            self.pitch = self.notes[ch] + 12 * self.octave
            self.noteType = Note
            self.initialSilence = False
        elif ch in "oiu":
            if len(buffer) >= 2 and buffer[-2].lower() in self.notes:
                prevChar = buffer[-2].lower()
                self.pitch = self.notes[prevChar] + 12 * self.octave
                self.noteType = Note
            else:
                self.instrument = 124
            self.noteType = Note
        elif ch == " ":
            self.noteType = Rest
        elif ch == "+":
            if len(buffer) >= 4 and buffer[-4:-1] == "BPM":
                self.bpm += 80
                self.noteType = Note

            elif len(buffer) >= 2 and buffer[-2] == "R":
                self.octave = min(self.octave + 1, 5)
                self.noteType = Note
            else:
                self.volume = min(self.volume * 2, 127)
                self.noteType = Note
        elif ch == "-":
            if len(buffer) >= 2 and buffer[-2] == "R":
                self.octave = max(self.octave - 1, -5)
                self.noteType = Note
            else:
                self.volume = 40
                self.noteType = Note
        elif ch == "?":
            randomNote = "abcdefg"[random.randint(0, 6)]
            self.pitch = self.notes[randomNote] + 12 * self.octave
            self.noteType = Note
        elif ch == ";":
            self.bpm = random.randint(30, 127)
            self.noteType = Note
        elif ch == "\n":
            self.instrument = random.randint(1, 127)
            self.noteType = Control
        else:
            pass

        if self.initialSilence:
            self.noteType = Rest

        midiInfo = None
        if self.noteType is Note:
            midiInfo = Note(self.instrument, self.pitch, self.volume, self.bpm)
        elif self.noteType is Rest:
            midiInfo = Rest(self.bpm)
        else:
            midiInfo = Control()

        return midiInfo

    def createMIDIObject(self):
        midi = MIDIFile(1)
        track = 0
        time = 0
        duration = 1
        channel = 0

        for note in self.translatedNotes:
            midi.addTempo(track, time, note.bpm)
            if note is None:
                raise ValueError("Note is None")

            if isinstance(note, Note):
                midi.addProgramChange(track, channel, time, note.instrument)
                midi.addNote(track, channel, note.pitch, time, duration, note.volume)
                time += duration
            elif isinstance(note, Rest):
                time += 1
        return midi
