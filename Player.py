from MidiInfo import Note, Rest
import pygame.midi
import time
import Translator


class Player:
    def __init__(self):
        pygame.midi.init()
        self.player = pygame.midi.Output(0)

    def play(self, midi):
        if isinstance(midi, Note):
            self.player.set_instrument(midi.instrument)
            self.player.note_on(midi.pitch, midi.volume)
            time.sleep(60 / midi.bpm)
            self.player.note_off(midi.pitch, midi.volume)
        elif isinstance(midi, Rest):
            time.sleep(60 / midi.bpm)

    def __del__(self):
        del self.player
        pygame.midi.quit()
