import pygame
import pygame.mixer as mixer
import sys


if __name__ == "__main__":
    pygame.init()
    mixer.init()
    mixer.music.load(sys.argv[1])
    mixer.music.play()

    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Music Player")
    font = pygame.font.Font("freesansbold.ttf", 36)
    text = font.render("Press 'space' to pause, 'q' to quit: ", True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (width // 2, height // 2)

    while True:
        screen.fill((0, 0, 0))
        screen.blit(text, textRect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if mixer.music.get_busy():
                        mixer.music.pause()
                    else:
                        mixer.music.unpause()
                elif event.key == pygame.K_q:
                    sys.exit(0)
        pygame.display.update()
