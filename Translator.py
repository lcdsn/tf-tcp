import random
from File import File
from MidiInfo import Note, Rest
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
        self.BREAKSILENCE = False
        self.translatedNotes = []

    def reset(self):
        self.instrument = 0
        self.pitch = 0
        self.octave = 0
        self.volume = 40
        self.bpm = 60
        self.BREAKSILENCE = False
        self.translatedNotes = []

    def convertTextToMIDI(self, buffer: str) -> Note | Rest | None:
        if len(buffer) == 0:
            raise ValueError("Buffer is empty")

        if self.instrument == 124:
            self.instrument = 0

        ch = buffer[-1].lower()
        if ch in self.notes:
            self.pitch = self.notes[ch] + 12 * self.octave
            self.BREAKSILENCE = True
        elif ch in "oiu":
            if len(buffer) >= 2 and buffer[-2].lower() in self.notes:
                prevChar = buffer[-2].lower()
                self.pitch = self.notes[prevChar] + 12 * self.octave
            else:
                self.instrument = 124
        elif ch == " ":
            rest = Rest(self.bpm)
            self.translatedNotes.append(rest)
            return rest
        elif ch == "+":
            if len(buffer) >= 4 and buffer[-4:] == "BPM":
                self.bpm += 80
            elif len(buffer) >= 2 and buffer[-2] == "R":
                self.octave = min(self.octave + 1, 5)
            else:
                self.volume = min(self.volume * 2, 127)
        elif ch == "-":
            if len(buffer) >= 2 and buffer[-2] == "R":
                self.octave = max(self.octave - 1, -5)
            else:
                self.volume = 40
        elif ch == "?":
            randomNote = "abcdefg"[random.randint(0, 6)]
            self.pitch = self.notes[randomNote] + 12 * self.octave
            self.BREAKSILENCE = True
        elif ch == ";":
            self.bpm = random.randint(30, 127)
        else:
            pass

        if self.BREAKSILENCE:
            note = Note(self.instrument, self.pitch, self.volume, self.bpm)
            self.translatedNotes.append(note)
            return note

        rest = Rest(self.bpm)
        self.translatedNotes.append(rest)
        return rest

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
