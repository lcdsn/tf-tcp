import sys
import pygame

from UITextArea import TextArea
from Button import IconButton
from File import File
from Translator import Translator
from Player import Player
from MidiInfo import Note, Rest, Control

WIDTH = 600
HEIGHT = 600

PLAYING = False
WAITING = False

startTime = None


def callback():
    global PLAYING
    PLAYING = not PLAYING


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <inpug-file>")
        sys.exit(1)

    f = File(sys.argv[1])
    f.readFile()
    t = Translator()
    p = Player()

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Conversor MIDI")
    pygame.key.set_repeat(300, 50)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    area = TextArea(
        text=f.fileContent,
        size=(WIDTH, HEIGHT),
        padding=[15, 15, 45, 15],
        backgroundColor=(255, 255, 255),
        fontName="iosevka-regular.ttf",
        fontSize=30,
    )

    play = IconButton(
        pos=(WIDTH // 2 - 20, HEIGHT - 45),
        size=(40, 40),
        normalColor=(255, 255, 255),
        selectedColor=(255, 255, 255),
        clickedColor=(255, 255, 255),
        iconPath="assets/icon-play.png",
        callbackFunction=callback,
    )

    paused = IconButton(
        pos=(WIDTH // 2 - 20, HEIGHT - 45),
        size=(40, 40),
        normalColor=(255, 255, 255),
        selectedColor=(255, 255, 255),
        clickedColor=(255, 255, 255),
        iconPath="assets/icon-pause.png",
        callbackFunction=callback,
    )

    running = True
    while running:
        button = paused if PLAYING else play

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    PLAYING = not PLAYING

            if not PLAYING:
                area.resizeText(event)

            area.scrollBar(event)
            area.moveCursor(event)

        screen.fill((0, 0, 0))
        screen.blit(area.draw(), dest=screen.get_rect().topleft)
        screen.blit(button.draw(), dest=button.pos)

        if PLAYING:
            buffer = None
            if area.cursorPosition < 4:
                buffer = f.fileContent[: area.cursorPosition + 1]
            else:
                buffer = f.fileContent[
                    area.cursorPosition - 3 : area.cursorPosition + 1
                ]
            note = t.convertTextToMIDI(buffer)
            print(note)

            if isinstance(note, Note) or isinstance(note, Rest):
                if not WAITING:
                    startTime = pygame.time.get_ticks()
                    WAITING = True
                    p.play(note)

                else:
                    if pygame.time.get_ticks() - startTime >= 1000 * (60 / note.bpm):
                        WAITING = False
                        p.stopNote(note)
                        area.cursorPosition += 1
            else:
                area.cursorPosition += 1

        pygame.time.Clock().tick(60)

        pygame.display.update()
