import sys
import pygame

from os import listdir
from os.path import isfile, join
import mimetypes

from UIListButton import ListButtons
from UITextArea import TextArea
from Button import IconButton, TextButton
from File import File
from Translator import Translator
from Player import Player
from MidiInfo import Note, Rest, Control

WIDTH = 800
HEIGHT = 600

PLAYING = False
WAITING = False

startTime = None


def loadFile(fileName):
    f = File(fileName)
    f.readFile()
    return f


def callbackPause():
    global PLAYING
    PLAYING = not PLAYING


def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input-folder>")
        sys.exit(1)

    files = []
    for f in listdir(sys.argv[1]):
        fileName = join(sys.argv[1], f)
        if mimetypes.guess_type(fileName)[0] == "text/plain":
            files.append(fileName)

    if len(files) == 0:
        print("No files found in the input folder")
        sys.exit(1)

    f = loadFile(files[0])
    t = Translator()
    p = Player()

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("")
    pygame.key.set_repeat(300, 50)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    area = TextArea(
        pos=(215, 0),
        text=f.fileContent,
        size=(WIDTH - 215, HEIGHT),
        padding=[15, 15, 45, 15],
        backgroundColor=(255, 255, 255),
        fontName="iosevka-regular.ttf",
        fontSize=30,
    )

    play = IconButton(
        pos=(215 + (WIDTH - 215) // 2 - 20, HEIGHT - 45),
        size=(40, 40),
        normalColor=(255, 255, 255),
        selectedColor=(255, 255, 255),
        clickedColor=(255, 255, 255),
        iconPath="assets/icon-play.png",
        callbackFunction=callbackPause,
    )

    paused = IconButton(
        pos=(215 + (WIDTH - 215) // 2 - 20, HEIGHT - 45),
        size=(40, 40),
        normalColor=(255, 255, 255),
        selectedColor=(255, 255, 255),
        clickedColor=(255, 255, 255),
        iconPath="assets/icon-pause.png",
        callbackFunction=callbackPause,
    )

    def callbackLoadFile(fileName):
        nonlocal f

        f = loadFile(fileName)
        area.text = f.fileContent
        area.restart()
        t.reset()

    fileTree = ListButtons(
        pos=(0, 0),
        listItems=files,
        buttonModel=TextButton(
            title="",
            pos=(0, 0),
            offset=(0, 0),
            size=(200, 40),
            normalColor=(0, 0, 255),
            selectedColor=(255, 0, 0),
            clickedColor=(0, 0, 0),
            fontName="iosevka-regular.ttf",
            fontColor=(255, 255, 255),
            iconPath="assets/icon-file.png",
            borderRadius=5,
            callbackFunction=lambda instance: callbackLoadFile(instance.title),
        ),
        size=(215, HEIGHT),
        padding=[5, 5, 5, 5],
    )

    note = None

    global PLAYING, WAITING, startTime
    running = True
    while running:
        button = paused if PLAYING else play

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            button.handleEvent(event)
            fileTree.handleEvent(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    PLAYING = not PLAYING

            if not PLAYING:
                area.resizeText(event)

            area.scrollBar(event)
            area.moveCursor(event)

        screen.fill((0, 0, 0))
        screen.blit(area.draw(), dest=area.pos)
        screen.blit(button.draw(), dest=button.pos)
        screen.blit(fileTree.draw(), dest=fileTree.pos)

        if PLAYING:
            if not WAITING:
                buffer = f.getBuffer(area.cursorPosition)
                if not buffer:
                    PLAYING = False
                    area.cursorPosition = 0
                    t = Translator()
                    continue

                note = t.convertTextToMIDI(buffer)
                if isinstance(note, Note) or isinstance(note, Rest):
                    startTime = pygame.time.get_ticks()
                    WAITING = True
                    print(note)
                    p.play(note)
                elif isinstance(note, Control):
                    area.cursorPosition += 1
                    continue

            else:
                if pygame.time.get_ticks() - startTime >= 1000 * 60 / note.bpm:
                    WAITING = False
                    p.stopNote(note)
                    area.cursorPosition += 1

        pygame.time.Clock().tick(60)
        pygame.display.update()


if __name__ == "__main__":
    main()
