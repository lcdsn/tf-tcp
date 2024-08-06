from MidiInfo import Note, Rest, Control
import pygame.midi
import time


class Player:
    def __init__(self):
        pygame.midi.init()
        self.player = pygame.midi.Output(0)

    def play(self, midi):
        if isinstance(midi, Note):
            self.player.set_instrument(midi.instrument)
            self.player.note_on(midi.pitch, midi.volume)

    def stopNote(self, midi):
        if isinstance(midi, Note):
            self.player.note_off(midi.pitch, midi.volume)

    def __del__(self):
        del self.player
        pygame.midi.quit()
