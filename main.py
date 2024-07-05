import sys
import random

from midiutil import MIDIFile

notes = {
    "c": 60,
    "d": 62,
    "e": 64,
    "f": 65,
    "g": 67,
    "a": 69,
    "b": 71,
}

track = 0
channel = 0
time = 0
duration = 1
tempo = 60
bpm = 60
default_volume = 100
volume = default_volume
pitch = 0
octave = 0
instrument = 0


def createMidi(notesList, output_file):
    midi = MIDIFile(1)
    track = 0
    time = 0
    channel = 0

    for note, volume, duration, instrument, bpm in notesList:
        midi.addTempo(track, time, bpm)
        midi.addProgramChange(track, channel, time, instrument)
        midi.addNote(track, channel, note, time, duration, volume)
        time += duration

    with open(output_file, "wb") as output_file:
        midi.writeFile(output_file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py [file-name]")
        exit(0)

    notesList = []
    text = None

    try:
        with open(sys.argv[1], "r") as f:
            text = f.read()

    except FileNotFoundError:
        print("File not found")
        exit(0)

    prevChar = None

    for i in range(len(text)):
        ch = text[i].lower()
        if not ch:
            break

        if ch in notes:
            notesList.append(
                (notes[ch] + 12 * octave, volume, duration, instrument, bpm)
            )
            prevChar = ch

        elif ch in "oiu":
            if prevChar in notes:
                notesList.append(
                    (notes[prevChar] + 12 * octave, volume, duration, instrument, bpm)
                )
                prevChar = ch
            else:
                notesList.append((notes["c"] + 12 * octave, volume, duration, 124, bpm))

        elif ch == " ":
            notesList.append((0, 0, duration, 0, bpm))

        elif ch == "+":
            if text[i - 1] == "R":
                octave += 1
            elif text[i - 3 : i] == "BPM":
                bpm += 80
            else:
                volume = min(127, 2 * volume)

        elif ch == "-":
            if text[i - 1] == "R":
                octave -= 1
            else:
                volume = default_volume

        elif ch == "?":
            randomNote = "abcdefg"[random.randint(0, 6)]
            notesList.append(
                (notes[randomNote] + 12 * octave, volume, duration, instrument, bpm)
            )

        elif ch == "\n":
            instrument = random.randint(0, 127)

        elif ch == ";":
            bpm = random.randint(1, 127)

        else:
            continue

        time += 1

    print(notesList)
    createMidi(notesList, "test.mid")
